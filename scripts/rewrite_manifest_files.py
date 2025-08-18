"""
Rewrite (update) all manifest files.

This script runs the `write_manifest_files()` function on all dandiset versions, allowing us to
rewrite the manifest files. We needed to run this as a one-time script when we moved from our
development AWS account to the AWS Open Data account, thus changing the AWS S3 bucket our data is
stored in. Currently the asset manifest files (.jsonld and .yaml) contain the name of the bucket, so
this became out of date when we copied the data over and changed the bucket. This script runs an
update on the manifest files, fixing the bucket referenced the asset manifest files.

We are doing this using the heroku CLI to connect to our database and then write_manifest_files()

Usage:
    # Open an interactive bash shell inside the heroku dyno for the given app
    heroku run -a <heroku_app_name> bash

    # Open a Django shell
    ./manage.py shell_plus
    # Run the script by copying and pasting the code
"""

from __future__ import annotations

import click

from dandiapi.api.models import Version
from dandiapi.api.tasks import write_manifest_files

all_versions = Version.objects.values_list('id', flat=True)
all_versions_count = all_versions.count()
click.echo(f'version count is {all_versions_count}')

if all_versions_count > 0:
    for version_id in all_versions.iterator():
        write_manifest_files.delay(version_id)
else:
    click.echo('Found no versions.')
