# Generated by Django 4.2.23 on 2025-07-09 18:24
from __future__ import annotations

from django.db import migrations, models


def bootstrap_application_stats(apps, _):
    AssetBlob = apps.get_model('api.AssetBlob')
    ZarrArchive = apps.get_model('zarr.ZarrArchive')
    Dandiset = apps.get_model('api.Dandiset')
    Version = apps.get_model('api.Version')
    User = apps.get_model('auth.User')
    ApplicationStats = apps.get_model('api.ApplicationStats')

    dandiset_count = Dandiset.objects.count()
    published_dandiset_count = (
        Version.objects.exclude(version='draft').values('dandiset').distinct().count()
    )
    user_count = User.objects.filter(metadata__status='APPROVED').count()
    size = sum(
        cls.objects.filter(assets__versions__isnull=False)
        .distinct()
        .aggregate(size=models.Sum('size'))['size']
        or 0
        for cls in (AssetBlob, ZarrArchive)
    )

    ApplicationStats.objects.create(
        dandiset_count=dandiset_count,
        published_dandiset_count=published_dandiset_count,
        user_count=user_count,
        size=size,
    )


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0022_remove_assetblob_download_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationStats',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True, unique=True)),
                ('dandiset_count', models.PositiveIntegerField()),
                ('published_dandiset_count', models.PositiveIntegerField()),
                ('user_count', models.PositiveIntegerField()),
                ('size', models.PositiveBigIntegerField()),
            ],
            options={
                'ordering': ['timestamp'],
                'verbose_name_plural': 'Application Stats',
            },
        ),
        migrations.RunPython(
            code=bootstrap_application_stats, reverse_code=migrations.RunPython.noop
        ),
    ]
