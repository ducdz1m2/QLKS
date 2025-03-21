# Generated by Django 5.1.6 on 2025-03-07 10:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('service', '0001_dichvu_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='HoaDon',
            fields=[
                ('MaHoaDon', models.AutoField(primary_key=True, serialize=False)),
                ('NgayLapHoaDon', models.DateField()),
                ('TongTien', models.DecimalField(decimal_places=2, max_digits=15)),
                ('MaSuDung', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='service.sudungdichvu', verbose_name='Mã Sử Dụng')),
            ],
        ),
    ]
