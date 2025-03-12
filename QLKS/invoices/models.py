from django.db import models
# from service.models import SuDungDichVu
from customer.models import ThuePhong
# Create your models here.

class HoaDon(models.Model):
    MaHoaDon = models.AutoField(primary_key=True)
    MaThue = models.ForeignKey(ThuePhong, on_delete=models.CASCADE,verbose_name="Mã thuê",  default=1)
    NgayLapHoaDon = models.DateField()
    TongTien = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.MaHoaDon} - {self.MaThue} - {self.NgayLapHoaDon} - {self.TongTien}"