# Generated by Django 5.0.6 on 2024-06-14 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0017_knockedusers'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='knock_count',
            field=models.IntegerField(null=True),
        ),
    ]
