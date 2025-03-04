from django.db import models

class NhanVien(models.Model):
    MaNhanVien = models.AutoField(primary_key=True)
    HoTen = models.CharField(max_length=100)
    NgaySinh = models.DateField()
    SoDienThoai = models.CharField(max_length=12)

