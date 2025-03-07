from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('nhanvien', 'Nhân viên'),
        ('khachhang', 'Khách hàng'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='khachhang')

    def is_nhanvien(self):
        return self.role == 'nhanvien'

    def is_khachhang(self):
        return self.role == 'khachhang'
