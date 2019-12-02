# Generated by Django 2.0.13 on 2019-11-23 13:13

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iati', '0068_point_srs_name_null_true'),
    ]

    operations = [
        migrations.CreateModel(
            name='NameSpaceElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_element_name', models.TextField()),
                ('parent_element_id', models.IntegerField()),
                ('namespace', django.contrib.postgres.fields.jsonb.JSONField(default=None, null=True)),
                ('nsmap', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
            ],
        ),
    ]
