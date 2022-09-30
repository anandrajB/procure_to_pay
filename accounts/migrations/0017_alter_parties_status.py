# Generated by Django 3.2.5 on 2022-09-30 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_counterparty_onboarding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parties',
            name='status',
            field=models.CharField(choices=[('NONE', 'NONE'), ('NEW', 'NEW'), ('IN_PROGRESS', 'IN_PROGRESS'), ('ONBOARDED', 'ONBOARDED'), ('DEACTIVATED', 'DEACTIVATED')], max_length=255),
        ),
    ]
