from __future__ import annotations

from django.conf import settings
import pytest

from dandiapi.analytics.models import ProcessedS3Log
from dandiapi.analytics.tasks import collect_s3_log_records_task, process_s3_log_file_task
from dandiapi.api.storage import create_s3_storage, get_boto_client


@pytest.fixture
def s3_log_bucket():
    return create_s3_storage(settings.DANDI_DANDISETS_LOG_BUCKET_NAME).bucket_name


@pytest.fixture
def s3_log_file(s3_log_bucket, asset_blob):
    s3 = get_boto_client()

    log_file_name = '2019-02-06-00-00-38-5C5B0E0CA8F2B1B5'
    s3.put_object(
        Bucket=s3_log_bucket,
        Key=log_file_name,
        # this is the minimum necessary structure for s3logparse to successfully parse the log
        Body=' '.join(
            [
                '-',
                '-',
                '[06/Feb/2019:00:00:38 +0000]',
                '-',
                '-',
                '-',
                'REST.GET.OBJECT',
                asset_blob.blob.name,
                '-',
                '200',
            ]
            + ['-'] * 10
        ),
    )

    yield log_file_name

    s3.delete_object(Bucket=s3_log_bucket, Key=log_file_name)


# TODO: add s3_log_bucket back in as a parameter
# def test_processing_s3_log_files(s3_log_bucket, s3_log_file, asset_blob):
@pytest.mark.django_db
def test_processing_s3_log_files(s3_log_file, asset_blob):
    # TODO: s3_log_bucket
    collect_s3_log_records_task()
    asset_blob.refresh_from_db()

    assert ProcessedS3Log.objects.count() == 1
    assert asset_blob.download_count == 1


# TODO: add s3_log_bucket back in as a parameter
# def test_processing_s3_log_files_idempotent(s3_log_bucket, s3_log_file, asset_blob):
@pytest.mark.django_db
def test_processing_s3_log_files_idempotent(s3_log_file, asset_blob):
    # this tests that the outer task which collects the log files to process is
    # idempotent, in other words, it uses StartAfter correctly.
    # TODO: s3_log_bucket
    collect_s3_log_records_task()
    # run the task again, it should skip the existing log record
    # TODO: s3_log_bucket
    collect_s3_log_records_task()
    asset_blob.refresh_from_db()

    assert ProcessedS3Log.objects.count() == 1
    assert asset_blob.download_count == 1


# TODO: add s3_log_bucket back in as a parameter
# def test_processing_s3_log_file_task_idempotent(s3_log_bucket, s3_log_file, asset_blob):
@pytest.mark.django_db
def test_processing_s3_log_file_task_idempotent(s3_log_file, asset_blob):
    # this tests that the inner task which processes a single log file is
    # idempotent, utilizing the unique constraint on ProcessedS3Log correctly.
    # TODO: s3_log_bucket
    process_s3_log_file_task(s3_log_file)
    # run the task again, it should ignore the new log
    # TODO: s3_log_bucket
    process_s3_log_file_task(s3_log_file)
    asset_blob.refresh_from_db()

    assert ProcessedS3Log.objects.count() == 1
    assert asset_blob.download_count == 1
