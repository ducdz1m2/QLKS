from django.db import models

# Create your models here.

class HoaDon(models.Model):
    MaHoaDon = models.AutoField(primary_key=True)
    MaSDDV = models.IntegerField()
    NgayLapHoaDon = models.DateField()
    TongTien = models.DecimalField(max_digits=15, decimal_places=2)
