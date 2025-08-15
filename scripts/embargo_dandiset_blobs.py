#
# This script will allow us to change blobs within a dandiset from public to embargoed.  It can also do the opposite and change  
# embargoed to public (to do the reverse you will need to comment out the first for loop and uncomment the second one)
# We are doing this using the heroku CLI to connect to our database.
# you will need the number of the dandi set, typically it looks like 6 number like 000037 you would put 37 on the 
# dandiset_id line below
# 
# TODO add the ability to check if a file is being referenced multiple times before changing it's emabargoed status.
#
# apps are currently ember-dandi-api and ember-dandi-api-sandbox
# heroku run -a <heroku_app_name> bash
# ./manage.py shell_plus


from botocore.config import Config

from dandiapi.api.models import AssetBlob, Dandiset, Version
from dandiapi.api.storage import get_boto_client
from dandiapi.api.models.asset import Asset
from django.conf import settings
from django.db import transaction

# Use the correct bucket below.  production or sandbox 
# BUCKET_NAME = 'ember-open-data'
BUCKET_NAME = 'ember-public-data-sandbox'

# this is the id of the dandiset, like 000037.  I am changed the ID to a dandiset that doesn't exist on emberdandi 
# so you will have to change to the correct one.
dandiset_id = 37

client = get_boto_client()

ds = Dandiset.objects.filter(id=dandiset_id).first()
if ds is None: 
    print("no id")

versions = ds.versions.all()

# to embargoed
with transaction.atomic():
    for version in versions.iterator():
        assets = version.assets
        print(f"version id: {version.id}")   
        for asset in assets.iterator():
            AssetBlob.objects.filter(blob_id=asset.blob.blob_id).update(embargoed=True)        
            print(f"   blob: {asset.blob.blob.name}")
            client.put_object_tagging(
                Bucket=BUCKET_NAME,
                Key=asset.blob.blob.name,
                Tagging={
                    'TagSet': [
                        {
                            'Key': 'embargoed',
                            'Value': 'true'
                        },
                    ]
                }
            )

# # to public
# with transaction.atomic():
#     for version in versions.iterator():
#         assets = version.assets
#         print(f"version id: {version.id}")   
#         for asset in assets.iterator():
#             AssetBlob.objects.filter(blob_id=asset.blob.blob_id).update(embargoed=False)        
#             print(f"   blob: {asset.blob.blob.name}")
#             client.delete_object_tagging(
#                             Bucket=BUCKET_NAME,
#                             Key=asset.blob.blob.name,
#                         )






