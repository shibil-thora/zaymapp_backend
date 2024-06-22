# Generated by Django 5.0.6 on 2024-06-04 21:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0016_alter_serviceimages_service'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='KnockedUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='knocks', to='services.service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='knocked_at', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]