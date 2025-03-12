from django.db import models
from customer.models import ThuePhong
# Create your models here.

class HoaDon(models.Model):
    MaHoaDon = models.AutoField(primary_key=True)
    MaSuDung = models.ForeignKey(ThuePhong, on_delete=models.CASCADE, default=1)
    NgayLapHoaDon = models.DateField()
    TongTien = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.MaHoaDon} - {self.MaSuDung} - {self.NgayLapHoaDon} - {self.TongTien}"