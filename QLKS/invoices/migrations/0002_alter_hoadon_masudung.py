# Generated by Django 5.1.6 on 2025-03-12 02:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_alter_thuephong_ngaytra'),
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoadon',
            name='MaSuDung',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='customer.thuephong', verbose_name='Mã Sử Dụng'),
        ),
    ]
