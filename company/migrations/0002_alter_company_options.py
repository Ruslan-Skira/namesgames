# Generated by Django 3.2.4 on 2022-02-08 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['last_parsed_at'], 'verbose_name_plural': 'Companies'},
        ),
    ]
