from django.db import models
<<<<<<< HEAD
=======
# from service.models import SuDungDichVu
>>>>>>> cc59e5759c9d77ad403a5ba20b6ba2ae9d5b0b2b
from customer.models import ThuePhong
# Create your models here.

class HoaDon(models.Model):
    MaHoaDon = models.AutoField(primary_key=True)
<<<<<<< HEAD
    MaThue = models.ForeignKey(ThuePhong, on_delete=models.CASCADE, default=1)
=======
    MaThue = models.ForeignKey(ThuePhong, on_delete=models.CASCADE,verbose_name="Mã thuê",  default=1)
>>>>>>> cc59e5759c9d77ad403a5ba20b6ba2ae9d5b0b2b
    NgayLapHoaDon = models.DateField()
    TongTien = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.MaHoaDon} - {self.MaThue} - {self.NgayLapHoaDon} - {self.TongTien}"