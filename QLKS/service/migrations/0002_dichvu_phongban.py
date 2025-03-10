# Generated by Django 5.1.6 on 2025-03-09 13:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_dichvu_migration'),
        ('staff', '0003_delete_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='dichvu',
            name='PhongBan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='staff.phongban'),
            preserve_default=False,
        ),
    ]
