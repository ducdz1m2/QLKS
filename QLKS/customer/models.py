from django.db import models
from room.models import Phong 
from accounts.models import CustomUser
# Create your models here.
class KhachHang(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    MaKhachHang = models.AutoField(primary_key=True)
    TenKhachHang = models.CharField(max_length=100)
    DiaChi = models.CharField(max_length=100)
    SoDienThoai = models.CharField(max_length=15)

class ThuePhong(models.Model):
    MaThue = models.AutoField(primary_key=True)
    MaKhachHang = models.ForeignKey(KhachHang, on_delete=models.CASCADE)
    MaPhong = models.ForeignKey(Phong, on_delete=models.CASCADE)
    NgayThue = models.DateTimeField()
    NgayNhan = models.DateTimeField()
    NgayTra = models.DateTimeField()
    TrangThai = [
        ('DA_DAT', 'Đã đặt'),
        ('DANG_O', 'Đang ở'),
        ('DA_TRA', 'Đã trả')
    ]