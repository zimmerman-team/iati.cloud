# Generated by Django 2.0.6 on 2018-07-19 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iati', '0009_auto_20180710_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentlink',
            name='result',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='iati.Result'),
        ),
    ]
