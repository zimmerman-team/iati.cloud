# Generated by Django 2.0.13 on 2019-09-04 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iati', '0064_auto_20190904_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='location_id_code',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]