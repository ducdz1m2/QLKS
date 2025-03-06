
from django.urls import path
from .views import *

urlpatterns = [
    path('',invoices_list, name='invoices_list'),
    path('invoices/',invoices_list, name='invoices_list'),
    path('add/',add_invoices, name='add_invoices'),
    path('delete/invoices/<int:MaHoaDon>', delete_invoices, name='delete_invoices'),
    path('edit/invoices/<int:MaHoaDon>', edit_invoices, name='edit_invoices'),
    path('detail/invoices/<int:MaHoaDon>',detail_invoices, name='detail_invoices'),
    # path('search/', search_invoices, name='search_invoices'),
]