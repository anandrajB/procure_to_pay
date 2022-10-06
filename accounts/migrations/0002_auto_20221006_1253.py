# Generated by Django 3.2.5 on 2022-10-06 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='signupprocess',
            old_name='address',
            new_name='address_line_1',
        ),
        migrations.AddField(
            model_name='signupprocess',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AlterField(
            model_name='signupprocess',
            name='party_type',
            field=models.CharField(choices=[('BUYER', 'BUYER')], default=1, max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='signupprocess',
            name='status',
            field=models.CharField(choices=[('NONE', 'NONE'), ('NEW', 'NEW'), ('IN_PROGRESS', 'IN_PROGRESS'), ('ONBOARDED', 'ONBOARDED'), ('DEACTIVATED', 'DEACTIVATED')], default=1, max_length=255),
            preserve_default=False,
        ),
    ]
