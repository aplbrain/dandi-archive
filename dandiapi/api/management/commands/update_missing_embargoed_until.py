from __future__ import annotations

import datetime
import logging

from django.utils import timezone
import djclick as click

from dandiapi.api.models.dandiset import Dandiset
from dandiapi.api.models.version import Version

logger = logging.getLogger(__name__)


@click.command()
def update_missing_embargoed_until():
    problem_dandisets = Dandiset.objects.filter(
        embargo_status='EMBARGOED', versions__metadata__access__0__embargoedUntil__isnull=True
    )

    dandisets_count = problem_dandisets.count()

    logger.info("Found %s dandisets with missing 'embargoedUntil'", dandisets_count)

    embargo_end_date = timezone.now().date() + datetime.timedelta(days=365 * 2)
    draft_versions = Version.objects.filter(version='draft', dandiset__in=problem_dandisets)
    for ver in draft_versions:
        ver.metadata['access'][0]['embargoedUntil'] = embargo_end_date.isoformat()
        ver.save()

    logger.info('Updated %s dandisets', dandisets_count)
