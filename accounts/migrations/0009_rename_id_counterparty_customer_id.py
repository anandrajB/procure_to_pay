# Generated by Django 3.2.5 on 2022-09-12 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_remove_counterparty_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='counterparty',
            old_name='id',
            new_name='customer_id',
        ),
    ]
