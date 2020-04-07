# Generated by Django 2.0.13 on 2020-03-17 15:16

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iati_synchroniser', '0016_datasetnote_last_updated_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='validation_md5',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='validation_status',
            field=django.contrib.postgres.fields.jsonb.JSONField(
                null=True, default=None),
        ),
    ]
