# Generated by Django 2.0.6 on 2018-10-29 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iati', '0048_remove_location_result_indicator_baseline'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='result_indicator_baseline',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='iati.ResultIndicatorBaseline'),
        ),
    ]
