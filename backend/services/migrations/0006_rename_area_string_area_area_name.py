# Generated by Django 5.0.6 on 2024-05-14 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_servicetype_service_serviceareas'),
    ]

    operations = [
        migrations.RenameField(
            model_name='area',
            old_name='area_string',
            new_name='area_name',
        ),
    ]
