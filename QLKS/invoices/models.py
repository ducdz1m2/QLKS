from django.db import models
# from service.models import SuDungDichVu
from customer.models import ThuePhong
# Create your models here.

class HoaDon(models.Model):
    TrangThaiHoaDon = [
        ('DA_THANH_TOAN', "Đã thanh toán"),
        ('CHUA_THANH_TOAN', "Chưa thanh toán")
    ]
    MaHoaDon = models.AutoField(primary_key=True)
    MaThue = models.ForeignKey(ThuePhong, on_delete=models.CASCADE,verbose_name="Mã thuê",  default=1)
    NgayLapHoaDon = models.DateField()
    TrangThai = models.CharField(
        choices=TrangThaiHoaDon,
        default='CHUA_THANH_TOAN',
        max_length=20
    )
    def __str__(self):
        return f"{self.MaHoaDon} - {self.MaThue} - {self.NgayLapHoaDon} - {self.TongTien}"