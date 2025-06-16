from __future__ import annotations

from django.core.validators import RegexValidator
from django.db import models


class ProcessedS3Log(models.Model):
    name = models.CharField(
        max_length=36,
        validators=[
            # https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerLogs.html#server-log-keyname-format
            RegexValidator(r'^\d{4}-(\d{2}-){5}[A-F0-9]{16}$')
        ],
    )

    # Represents if this s3 log file is private (including embargoed) or public.
    # If private is True, the log file lives in the S3 bucket pointed to by
    # DANDI_DANDISETS_PRIVATE_LOG_BUCKET_NAME.
    # If private is False...
    #   & historically_embargoed is False, the log file lives in the S3
    #   bucket pointed to by DANDI_DANDISETS_LOG_BUCKET_NAME.
    #   & historically_embargoed is True, the log file lives in the S3
    #   bucket pointed to by DANDI_DANDISETS_EMBARGO_LOG_BUCKET_NAME.
    private = models.BooleanField(default=False)

    # Represents if this s3 log file was embargoed prior to the embargo re-design.
    historically_embargoed = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'private', 'historically_embargoed'],
                name='%(app_label)s_%(class)s_unique_name_embargoed',
            )
        ]

    def __str__(self) -> str:
        return self.name
