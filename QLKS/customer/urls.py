from django.urls import path
from .views import *

urlpatterns = [
    path('', customer_list, name='customer_list'),
    path('rentroom/', rentroom_list, name='rentroom_list'),
    path('add/customer/', add_customer, name='add_customer'),
    path('edit/customer/<int:MaKhachHang>', edit_customer, name='edit_customer'),
    path('delete/customer/<int:MaKhachHang>', delete_customer, name='delete_customer'),
    path('detail/customer/<int:MaKhachHang>', detail_customer, name='detail_customer'),
]