# Generated by Django 3.2.5 on 2022-05-20 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20220520_1841'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parties',
            options={'ordering': ['id'], 'verbose_name_plural': 'Party'},
        ),
    ]
