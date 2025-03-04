from django.urls import path
from.views import invoices_list

urlpatterns = [
    path('',invoices_list, name='invoices_list'),
]
