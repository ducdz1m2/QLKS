from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):  
    is_staff_member = models.BooleanField(default=False)  # True nếu là nhân viên
    is_customer = models.BooleanField(default=False)      # True nếu là khách hàng