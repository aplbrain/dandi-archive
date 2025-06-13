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

    # TODO: We need another variable to tell us where this s3 log file lives
    # We will have 2 "active" buckets - private and open
    # However, DANDI will still have log files in the old embargoed log bucket

    # type of data -> Which bucket log file is located in
    # if private data -> log in Private bucket
    # if embargoed data ->
    #       * If (DANDI only) historically_embargoed -> log in Embargoed bucket
    #       if USE_PRIVATE = T -> log in Private bucket
    #       if USE_PRIVATE = F -> log in Open bucket
    # if open data ->
    #       if previously embargoed -> ?? does it matter
    #       else -> log in Open bucket

    # IDEA:
    # private = models.BooleanField(default=False)
    # if private -> private log bucket
    # if not private && historically_embargoed -> embargoed log bucket
    # if not private && not historically_embargoed -> open bucket

    # Represents if this s3 log file was embargoed prior to the embargo re-design.
    # If this field is True, the log file lives in the S3 bucket pointed to by the
    # DANDI_DANDISETS_EMBARGO_LOG_BUCKET_NAME setting.
    historically_embargoed = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'historically_embargoed'],
                name='%(app_label)s_%(class)s_unique_name_embargoed',
            )
        ]

    def __str__(self) -> str:
        return self.name
