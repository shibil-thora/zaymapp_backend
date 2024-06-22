# Generated by Django 5.0.6 on 2024-05-14 11:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_servicetype_service_serviceareas'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=100)),
                ('available', models.BooleanField(default=False)),
                ('permit', models.BooleanField(default=False)),
                ('description', models.TextField(max_length=500, null=True)),
                ('cover_image', models.ImageField(null=True, upload_to='covers')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to=settings.AUTH_USER_MODEL)),
                ('service_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.servicetype')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceAreas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='areas', to='services.service')),
            ],
        ),
    ]
