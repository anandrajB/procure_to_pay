# Generated by Django 3.2.5 on 2022-10-06 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20221006_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupprocess',
            name='party_type',
            field=models.CharField(default='BUYER', max_length=25),
        ),
    ]