"""
Rewrite (update) all manifest files.

This will allow us to rewrite the manifest files.  Currently the asset manifest files .jsonid and yaml contain the name of the bucket.
when moving to AWS Open Data bucket we are copying all the data over to the new bucket.  Now we need to change the manifest files to reflect that.
We are doing this using the heroku CLI to connect to our database and then write_manifest_files()

Usage:
    # Open an interactive bash shell inside the heroku dyno for the given app
    heroku run -a <heroku_app_name> bash

    # Run the script directly
    ./manage.py rewrite_manifest_files.py
    # OR
    # Open a Django shell
    ./manage.py shell_plus
    # And run the script by copying and pasting the code
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
