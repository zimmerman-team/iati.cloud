# Generated by Django 2.0.13 on 2020-07-30 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iati_synchroniser', '0017_auto_20200317_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='iati_version',
            field=models.CharField(default='2.02', max_length=255),
        ),
    ]
