# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 15:54
from __future__ import unicode_literals

from django.db import migrations, models
from django.contrib.contenttypes.management import update_contenttypes
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iati_codelists', '0003_auto_20160204_1305'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('iati_organisation', '0002_remove_organisations'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganisationNarrative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField(db_index=True, verbose_name=b'related object')),
                ('content', models.TextField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iati_codelists.Language')),
            ],
        ),
        migrations.RenameModel(
            old_name='Name',
            new_name='OrganisationName',
        ),
        migrations.RenameModel(
            old_name='ReportingOrg',
            new_name='OrganisationReportingOrganisation',
        ),
        migrations.RemoveField(
            model_name='narrative',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='narrative',
            name='language',
        ),
        migrations.RenameField(
            model_name='organisation',
            old_name='iati_version',
            new_name='iati_standard_version',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='abbreviation',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='code',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='original_ref',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='type',
        ),
        migrations.AddField(
            model_name='organisation',
            name='id',
            field=models.CharField(max_length=150, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organisation',
            name='reported_in_iati',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='budgetline',
            name='organisation_identifier',
            field=models.CharField(max_length=150, null=True, verbose_name=b'organisation_identifier'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='last_updated_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='organisation_identifier',
            field=models.CharField(db_index=True, max_length=150),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Narrative',
        ),
        migrations.AddField(
            model_name='organisationnarrative',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iati_organisation.Organisation'),
        ),
        migrations.AlterIndexTogether(
            name='organisationnarrative',
            index_together=set([('content_type', 'object_id')]),
        ),
    ]
