from django.db import models
from service.models import SuDungDichVu
# Create your models here.

class HoaDon(models.Model):
    MaHoaDon = models.AutoField(primary_key=True)
    MaSuDung = models.ForeignKey(SuDungDichVu, on_delete=models.CASCADE,verbose_name="Mã Sử Dụng",  default=1)
    NgayLapHoaDon = models.DateField()
    TongTien = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.MaHoaDon} - {self.MaSuDung} - {self.NgayLapHoaDon} - {self.TongTien}"