# Generated by Django 4.2.20 on 2025-04-14 12:19
from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0018_auditrecord_admin_auditrecord_description_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='asset',
            index=models.Index(
                condition=models.Q(('status', 'Pending')),
                fields=['status'],
                name='api_asset_status_pending',
            ),
        ),
    ]
