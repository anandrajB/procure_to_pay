# Generated by Django 3.2.5 on 2022-05-17 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workevents',
            name='action',
            field=models.CharField(default='SAVE', max_length=25),
        ),
        migrations.AddField(
            model_name='workevents',
            name='subaction',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]
