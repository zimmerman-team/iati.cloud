# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-02 17:46
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iati_vocabulary', '0004_auto_20160602_1726'),
        ('iati_organisation', '0006_auto_20160602_1104'),
        ('iati_codelists', '0005_auto_20160602_1644'),
        ('iati', '0035_auto_20160531_0246'),
    ]

    operations = [
        migrations.CreateModel(
            name='HumanitarianScope',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('vocabulary_uri', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlannedDisbursementProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(blank=True, default=b'', max_length=250)),
                ('normalized_ref', models.CharField(default=b'', max_length=120)),
                ('provider_activity_ref', models.CharField(blank=True, db_index=True, default=b'', max_length=200, null=True, verbose_name=b'provider-activity-id')),
                ('primary_name', models.CharField(blank=True, db_index=True, default=b'', max_length=250)),
                ('organisation', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='planned_disbursement_providing_organisation', to='iati_organisation.Organisation')),
            ],
        ),
        migrations.CreateModel(
            name='PlannedDisbursementReceiver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(blank=True, default=b'', max_length=250)),
                ('normalized_ref', models.CharField(default=b'', max_length=120)),
                ('receiver_activity_ref', models.CharField(blank=True, db_index=True, default=b'', max_length=200, null=True, verbose_name=b'receiver-activity-id')),
                ('primary_name', models.CharField(blank=True, db_index=True, default=b'', max_length=250)),
                ('organisation', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='planned_disbursement_receiving_organisation', to='iati_organisation.Organisation')),
            ],
        ),
        migrations.RemoveField(
            model_name='planneddisbursement',
            name='budget_type',
        ),
        migrations.AddField(
            model_name='activity',
            name='humanitarian',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='activityparticipatingorganisation',
            name='org_activity_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activity_id', to='iati.Activity'),
        ),
        migrations.AddField(
            model_name='activitypolicymarker',
            name='vocabulary_uri',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='activityrecipientregion',
            name='vocabulary_uri',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='activitysector',
            name='vocabulary_uri',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='budget',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='iati_codelists.BudgetStatus'),
        ),
        migrations.AddField(
            model_name='planneddisbursement',
            name='cad_value',
            field=models.DecimalField(decimal_places=7, default=Decimal('0'), max_digits=20),
        ),
        migrations.AddField(
            model_name='planneddisbursement',
            name='eur_value',
            field=models.DecimalField(decimal_places=7, default=Decimal('0'), max_digits=20),
        ),
        migrations.AddField(
            model_name='planneddisbursement',
            name='gbp_value',
            field=models.DecimalField(decimal_places=7, default=Decimal('0'), max_digits=20),
        ),
        migrations.AddField(
            model_name='planneddisbursement',
            name='jpy_value',
            field=models.DecimalField(decimal_places=7, default=Decimal('0'), max_digits=20),
        ),
        migrations.AddField(
            model_name='planneddisbursement',
            name='type',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='iati_codelists.BudgetType'),
        ),
        migrations.AddField(
            model_name='planneddisbursement',
            name='usd_value',
            field=models.DecimalField(decimal_places=7, default=Decimal('0'), max_digits=20),
        ),
        migrations.AlterField(
            model_name='activitypolicymarker',
            name='significance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='iati_codelists.PolicySignificance'),
        ),
        migrations.AlterField(
            model_name='planneddisbursement',
            name='period_end',
            field=models.DateField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='planneddisbursement',
            name='period_start',
            field=models.DateField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='planneddisbursement',
            name='value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='planneddisbursement',
            name='value_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='planneddisbursementreceiver',
            name='planned_disbursement',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='receiver_organisation', to='iati.PlannedDisbursement'),
        ),
        migrations.AddField(
            model_name='planneddisbursementreceiver',
            name='receiver_activity',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='planned_disbursement_receiver_activity', to='iati.Activity'),
        ),
        migrations.AddField(
            model_name='planneddisbursementprovider',
            name='planned_disbursement',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='provider_organisation', to='iati.PlannedDisbursement'),
        ),
        migrations.AddField(
            model_name='planneddisbursementprovider',
            name='provider_activity',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='planned_disbursement_provider_activity', to='iati.Activity'),
        ),
        migrations.AddField(
            model_name='humanitarianscope',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iati.Activity'),
        ),
        migrations.AddField(
            model_name='humanitarianscope',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iati_codelists.HumanitarianScopeType'),
        ),
        migrations.AddField(
            model_name='humanitarianscope',
            name='vocabulary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iati_vocabulary.HumanitarianScopeVocabulary'),
        ),
    ]
