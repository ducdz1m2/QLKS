from django.db import models

class LoaiPhong(models.Model):
    MaLoai = models.AutoField(primary_key=True)
    TenLoai = models.CharField(max_length=50)
    GiaPhong = models.DecimalField(max_digits=10, decimal_places=2)

class Phong(models.Model):

    TRANG_THAI_CHOICES = [
        ('TRONG', 'Trống'),
        ('SU_DUNG', 'Đang sử dụng'),
    ]
    MaPhong = models.AutoField(primary_key=True)
    MaLoai = models.ForeignKey(LoaiPhong, on_delete=models.CASCADE)
    SoPhong = models.CharField(max_length=10)
    TrangThai = models.CharField(
        max_length=20,
        choices=TRANG_THAI_CHOICES,
        default='TRONG'
    )
    
