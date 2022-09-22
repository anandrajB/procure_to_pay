# Generated by Django 3.2.5 on 2022-09-21 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_parties_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parties',
            name='status',
            field=models.CharField(choices=[('NEW', 'NEW'), ('IN_PROGRESS', 'IN_PROGRESS'), ('ONBOARDED', 'ONBOARDED'), ('DEACTIVATED', 'DEACTIVATED')], default='NEW', max_length=255),
        ),
    ]