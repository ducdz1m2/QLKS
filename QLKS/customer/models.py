from django.db import models
from room.models import Phong 
from accounts.models import CustomUser

class KhachHang(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    TenKhachHang = models.CharField(max_length=100)
    SoDienThoai = models.CharField(max_length=15)
    DiaChi = models.CharField(max_length=100)
    Diem = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)

class ThuePhong(models.Model):
    khach_hang = models.ForeignKey(KhachHang, on_delete=models.CASCADE)  # Thêm lại khóa ngoại
    phong = models.ForeignKey(Phong, on_delete=models.CASCADE)  # Thêm lại khóa ngoại
    NgayThue = models.DateTimeField()
    NgayNhan = models.DateTimeField() 
    NgayTra = models.DateTimeField(null=True, blank=True) # Cho phép null vì chưa biết ngày trả lúc đặt
    TRANG_THAI_CHOICES = [
        ('DA_DAT', 'Đã đặt'),
        ('DANG_O', 'Đang ở'),
        ('DA_TRA', 'Đã trả')
    ]
    TrangThai = models.CharField(max_length=10, choices=TRANG_THAI_CHOICES)
