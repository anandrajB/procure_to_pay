# Generated by Django 3.2.5 on 2022-09-26 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0004_alter_pairings_counterparty_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='pairings',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='programs',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]
