from django.db import models
from customer.models import ThuePhong
from staff.models import PhongBan
class DichVu(models.Model):
    MaDichVu = models.AutoField(primary_key=True, verbose_name="Mã Dịch Vụ")
    TenDichVu = models.CharField(max_length=100, verbose_name="Tên Dịch Vụ")
    GiaDichVu = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Giá Dịch Vụ")
    PhongBan = models.ForeignKey(PhongBan, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.MaDichVu} - {self.TenDichVu} - {self.GiaDichVu}"

class SuDungDichVu(models.Model):
    TrangThai = [
        ('CHO_XU_LY', 'Chờ xử lý'),
        ('DANG_XU_LY', 'Đang xử lý'),
        ('HOAN_THANH', 'Hoàn thành')
    ]
    MaSuDung = models.AutoField(primary_key=True, verbose_name="Mã Sử Dụng")
    MaThue = models.ForeignKey(ThuePhong, on_delete=models.CASCADE, verbose_name="Mã Thuê")
    MaDichVu = models.ForeignKey(DichVu, on_delete=models.CASCADE, verbose_name="Mã Dịch Vụ")
    NgaySuDung = models.DateField(null=True, blank=True, verbose_name="Ngày Sử Dụng")
    TrangThai = models.CharField(
        choices=TrangThai,
        max_length=20,
        default='CHO_XU_LY'
    )
    def __str__(self):
        return f"{self.MaSuDung} - {self.MaThue} - {self.MaDichVu} - {self.SoLuong} - {self.NgaySuDung}"