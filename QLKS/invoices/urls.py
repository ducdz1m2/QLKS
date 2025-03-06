
from django.urls import path
from .views import *

urlpatterns = [
    path('',invoices_list, name='invoices_list'),
    path('add/',add_invoices, name='add_invoices'),
    path('delete/<int:MaHoaDon>', delete_invoices, name='delete_invoices'),
    path('edit/<int:MaHoaDon>', edit_invoices, name='edit_invoices'),
    path('detail/<int:MaHoaDon>',detail_invoices, name='detail_invoices'),
    # path('search/', search_invoices, name='search_invoices'),
]