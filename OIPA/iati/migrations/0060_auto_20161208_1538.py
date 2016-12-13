# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-12-08 15:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iati', '0060_remove_country_budget_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='countrybudgetitem',
            name='percentage',
        ),
        migrations.AlterField(
            model_name='budgetitemdescription',
            name='budget_item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='description', to='iati.BudgetItem'),
        ),
        migrations.AlterField(
            model_name='countrybudgetitem',
            name='activity',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='country_budget_items', to='iati.Activity'),
        ),
        migrations.AlterField(
            model_name='transactionrecipientcountry',
            name='transaction',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_country', to='iati.Transaction'),
        ),
        migrations.AlterField(
            model_name='transactionrecipientregion',
            name='transaction',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_region', to='iati.Transaction'),
        ),
    ]
