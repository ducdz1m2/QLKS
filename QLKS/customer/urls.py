from django.urls import path
from .views import *

urlpatterns = [
    path('', customer_list, name='customer_list'),
    path('add/', add_customer, name='add_customer'),
    path('edit/<int:MaKhachHang>', edit_customer, name='edit_customer'),
    path('delete/<int:MaKhachHang>', delete_customer, name='delete_customer'),
    path('detail/<int:MaKhachHang>', detail_customer, name='detail_customer'),
]