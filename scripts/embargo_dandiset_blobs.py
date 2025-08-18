"""
Embargo dandiset blobs (files) in the S3 bucket and in the database.

This script will allow us to change blobs within a dandiset from public to embargoed. It can also do
the opposite and change embargoed to public (to do the reverse you will need to comment out the
first for loop and uncomment the second one).

We are doing this using the heroku CLI to connect to our database.

Note:
    Before running, you will need to set the BUCKET_NAME and DANDISET_ID accordingly.

Usage:
    # Open an interactive bash shell inside the heroku dyno for the given app
    heroku run -a <heroku_app_name> bash

    # Open a Django shell
    ./manage.py shell_plus
    # Run the script by copying and pasting the code
"""

from __future__ import annotations

import click
from django.db import transaction

from dandiapi.api.models import AssetBlob, Dandiset
from dandiapi.api.storage import get_boto_client

# === CHANGE THIS SECTION ===
# S3 Bucket Name (production vs. sandbox)
# BUCKET_NAME = 'ember-open-data'
BUCKET_NAME = 'ember-public-data-sandbox'

# Id of the Dandiset for blobs to embargo. Ex) 000037 -> 37
DANDISET_ID = None
# === END SECTION ===

client = get_boto_client()

ds = Dandiset.objects.filter(id=DANDISET_ID).first()
if ds is None:
    click.echo('no id')

versions = ds.versions.all()

# Set Files in Dandiset to Embargoed
with transaction.atomic():
    for version in versions.iterator():
        assets = version.assets
        click.echo(f'version id: {version.id}')
        for asset in assets.iterator():
            AssetBlob.objects.filter(blob_id=asset.blob.blob_id).update(embargoed=True)
            click.echo(f'   blob: {asset.blob.blob.name}')
            client.put_object_tagging(
                Bucket=BUCKET_NAME,
                Key=asset.blob.blob.name,
                Tagging={
                    'TagSet': [
                        {'Key': 'embargoed', 'Value': 'true'},
                    ]
                },
            )

# # Set Files in Dandiset to Public
# with transaction.atomic():
#     for version in versions.iterator():
#         assets = version.assets
#         click.echo(f"version id: {version.id}")
#         for asset in assets.iterator():
#             AssetBlob.objects.filter(blob_id=asset.blob.blob_id).update(embargoed=False)
#             click.echo(f"   blob: {asset.blob.blob.name}")
#             client.delete_object_tagging(
#                             Bucket=BUCKET_NAME,
#                             Key=asset.blob.blob.name,
#                         )
