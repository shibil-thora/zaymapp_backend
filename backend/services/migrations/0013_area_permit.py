# Generated by Django 5.0.6 on 2024-05-28 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0012_alter_servicetype_is_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='permit',
            field=models.BooleanField(default=True),
        ),
    ]
