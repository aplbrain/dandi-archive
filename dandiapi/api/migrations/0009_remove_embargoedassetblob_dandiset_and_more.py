# Generated by Django 4.1.13 on 2024-01-16 18:31
from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0008_migrate_embargoed_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='embargoedassetblob',
            name='dandiset',
        ),
        migrations.RemoveField(
            model_name='embargoedupload',
            name='dandiset',
        ),
        migrations.RemoveConstraint(
            model_name='asset',
            name='exactly-one-blob',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='embargoed_blob',
        ),
        migrations.AddConstraint(
            model_name='asset',
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(('blob__isnull', True), ('zarr__isnull', False)),
                    models.Q(('blob__isnull', False), ('zarr__isnull', True)),
                    _connector='OR',
                ),
                name='blob-xor-zarr',
            ),
        ),
        migrations.DeleteModel(
            name='EmbargoedAssetBlob',
        ),
        migrations.DeleteModel(
            name='EmbargoedUpload',
        ),
    ]
