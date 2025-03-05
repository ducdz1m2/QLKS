from django.db import models

class DichVu(models.Model):
    MaDichVu = models.AutoField(primary_key=True)
    TenDichVu = models.CharField(max_length=100)
    GiaDichVu = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.TenDichVu