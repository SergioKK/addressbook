# Generated by Django 3.2.7 on 2021-10-02 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_rename_url_contact_contact_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='static/images'),
        ),
    ]