from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor, wait
import json
from typing import TYPE_CHECKING

from celery.utils.log import get_task_logger
from django.core import serializers
from django.db import transaction
from django.utils import timezone
from more_itertools import chunked

from dandiapi import settings
from dandiapi.api.models import (
    GarbageCollectionEvent,
    GarbageCollectionEventRecord,
    Upload,
)
from dandiapi.api.models.upload import PrivateUpload, PublicUpload
from dandiapi.api.storage import DandiMultipartMixin

if TYPE_CHECKING:
    from django.db.models import QuerySet

logger = get_task_logger(__name__)

UPLOAD_EXPIRATION_TIME = DandiMultipartMixin._url_expiration  # noqa: SLF001


def get_queryset() -> QuerySet[Upload]:
    """Get the queryset of Uploads that are eligible for garbage collection."""
    return get_public_queryset().union(get_private_queryset())


def get_public_queryset() -> QuerySet[PublicUpload]:
    """Get the queryset of PublicUploads that are eligible for garbage collection."""
    return PublicUpload.objects.filter(
        created__lt=timezone.now() - UPLOAD_EXPIRATION_TIME,
    )


def get_private_queryset() -> QuerySet[PrivateUpload]:
    """Get the queryset of PrivateUploads that are eligible for garbage collection."""
    return PrivateUpload.objects.filter(
        created__lt=timezone.now() - UPLOAD_EXPIRATION_TIME,
    )


def _garbage_collect(qs: QuerySet[Upload], UploadModel: type[PublicUpload | PrivateUpload]):  # noqa: N803
    from . import GARBAGE_COLLECTION_EVENT_CHUNK_SIZE  # noqa: PLC0415

    if not qs.exists():
        return 0

    deleted_records = 0
    futures: list[Future] = []

    with transaction.atomic(), ThreadPoolExecutor() as executor:
        event = GarbageCollectionEvent.objects.create(type=UploadModel.__name__)
        for uploads_chunk in chunked(qs.iterator(), GARBAGE_COLLECTION_EVENT_CHUNK_SIZE):
            GarbageCollectionEventRecord.objects.bulk_create(
                GarbageCollectionEventRecord(
                    event=event, record=json.loads(serializers.serialize('json', [u]))[0]
                )
                for u in uploads_chunk
            )

            # Delete the blobs from S3
            futures.append(
                executor.submit(
                    lambda chunk: [u.blob.delete(save=False) for u in chunk],
                    uploads_chunk,
                )
            )

            deleted_records += UploadModel.objects.filter(
                pk__in=[u.pk for u in uploads_chunk],
            ).delete()[0]

        wait(futures)

    return deleted_records


def garbage_collect() -> int:
    public_qs = get_public_queryset()
    deleted_records = _garbage_collect(public_qs, PublicUpload)

    if settings.ALLOW_PRIVATE:
        private_qs = get_private_queryset()
        deleted_records += _garbage_collect(private_qs, PrivateUpload)

    return deleted_records
