# Generated by Django 3.2.5 on 2022-05-23 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0008_alter_workevents_record_datas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workevents',
            name='record_datas',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
