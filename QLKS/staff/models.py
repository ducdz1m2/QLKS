from django.db import models
from accounts.models import CustomUser 


class PhongBan(models.Model):
    MaPhongBan = models.AutoField(primary_key=True)
    TenPhongBan = models.CharField(max_length=100)
    
class NhanVien(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    MaNhanVien = models.AutoField(primary_key=True)
    HoTen = models.CharField(max_length=100)
    NgaySinh = models.DateField()
    SoDienThoai = models.CharField(max_length=12)
    MaPhongBan = models.ForeignKey(PhongBan, on_delete=models.CASCADE)

