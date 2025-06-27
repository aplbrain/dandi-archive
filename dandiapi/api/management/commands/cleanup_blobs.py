from __future__ import annotations

from django.conf import settings
import djclick as click
from storages.backends.s3 import S3Storage

from dandiapi.api.models.upload import PrivateAssetBlob, PublicAssetBlob

BUCKET = settings.DANDI_DANDISETS_BUCKET_NAME
PRIVATE_BUCKET = settings.DANDI_DANDISETS_BUCKET_NAME


def s3_client():
    storage = S3Storage(bucket_name=BUCKET)
    return storage.connection.meta.client


def s3_client_private():
    storage = S3Storage(bucket_name=PRIVATE_BUCKET)
    return storage.connection.meta.client


def _cleanup_blobs(*, delete: bool, private: bool):
    bucket_name = BUCKET if not private else PRIVATE_BUCKET
    client = s3_client() if not private else s3_client_private()
    BlobModel = PublicAssetBlob if not private else PrivateAssetBlob  # noqa: N806

    # Ignore pagination for now, hopefully there aren't enough objects to matter
    objs = client.list_object_versions(Bucket=bucket_name, Prefix='dev/')
    for version in objs['Versions']:
        if not BlobModel.objects.filter(etag=version['ETag'][1:-1]).exists():
            click.echo(f'Deleting version {version["Key"]}')
            if delete:
                client.delete_object(
                    Bucket=bucket_name, Key=version['Key'], VersionId=version['VersionId']
                )
    for delete_marker in objs['DeleteMarkers']:
        click.echo(f'Deleting delete marker {delete_marker["Key"]}')
        if delete:
            client.delete_object(
                Bucket=bucket_name, Key=delete_marker['Key'], VersionId=delete_marker['VersionId']
            )


@click.command()
@click.option('--delete', is_flag=True, default=False)
def cleanup_blobs(*, delete: bool):
    _cleanup_blobs(delete=delete, private=False)
    if settings.ALLOW_PRIVATE:
        _cleanup_blobs(delete=delete, private=True)
