from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor, wait
from datetime import timedelta
import json
from typing import TYPE_CHECKING

from celery.utils.log import get_task_logger
from django.core import serializers
from django.db import transaction
from django.utils import timezone
from more_itertools import chunked

from dandiapi import settings
from dandiapi.api.models import (
    AssetBlob,
    GarbageCollectionEvent,
    GarbageCollectionEventRecord,
)
from dandiapi.api.models.asset import PrivateAssetBlob, PublicAssetBlob

if TYPE_CHECKING:
    from django.db.models import QuerySet

logger = get_task_logger(__name__)

ASSET_BLOB_EXPIRATION_TIME = timedelta(days=7)


def get_queryset() -> QuerySet[AssetBlob]:
    """Get the queryset of AssetBlobs that are eligible for garbage collection."""
    return get_public_queryset().union(get_private_queryset())


def get_public_queryset() -> QuerySet[PublicAssetBlob]:
    """Get the queryset of PublicAssetBlobs that are eligible for garbage collection."""
    return PublicAssetBlob.objects.filter(
        assets__isnull=True,
        created__lt=timezone.now() - ASSET_BLOB_EXPIRATION_TIME,
    )


def get_private_queryset() -> QuerySet[PrivateAssetBlob]:
    """Get the queryset of PrivateAssetBlobs that are eligible for garbage collection."""
    return PrivateAssetBlob.objects.filter(
        assets__isnull=True,
        created__lt=timezone.now() - ASSET_BLOB_EXPIRATION_TIME,
    )


def _garbage_collect(
    qs: QuerySet[AssetBlob],
    BlobModel: type[PublicAssetBlob | PrivateAssetBlob],  # noqa: N803
) -> int:
    from . import GARBAGE_COLLECTION_EVENT_CHUNK_SIZE

    if not qs.exists():
        return 0

    deleted_records = 0
    futures: list[Future] = []

    with transaction.atomic(), ThreadPoolExecutor() as executor:
        event = GarbageCollectionEvent.objects.create(type=BlobModel.__name__)
        for asset_blobs_chunk in chunked(qs.iterator(), GARBAGE_COLLECTION_EVENT_CHUNK_SIZE):
            GarbageCollectionEventRecord.objects.bulk_create(
                GarbageCollectionEventRecord(
                    event=event, record=json.loads(serializers.serialize('json', [a]))[0]
                )
                for a in asset_blobs_chunk
            )

            # Delete the blobs from S3
            futures.append(
                executor.submit(
                    lambda chunk: [a.blob.delete(save=False) for a in chunk],
                    asset_blobs_chunk,
                )
            )

            deleted_records += BlobModel.objects.filter(
                pk__in=[a.pk for a in asset_blobs_chunk],
            ).delete()[0]

        wait(futures)

    return deleted_records


def garbage_collect() -> int:
    public_qs = get_public_queryset()
    deleted_records = _garbage_collect(public_qs, PublicAssetBlob)

    if settings.ALLOW_PRIVATE:
        private_qs = get_private_queryset()
        deleted_records += _garbage_collect(private_qs, PrivateAssetBlob)

    return deleted_records
