# Generated by Django 3.2.5 on 2022-09-14 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('transaction', '0003_alter_pairings_counterparty_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pairings',
            name='counterparty_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.parties'),
        ),
    ]
