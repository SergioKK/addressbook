# Generated by Django 3.2.7 on 2021-09-29 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='url',
            new_name='contact_url',
        ),
    ]
