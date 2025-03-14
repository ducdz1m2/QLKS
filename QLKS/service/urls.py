from django.urls import path
from .views import *

urlpatterns = [
    #Dich vu
    path('', service_list, name='service_list'),
    path('add/', add_service, name='add_service'),
    path('edit/<int:pk>/', edit_service, name='edit_service'),
    path('delete/<int:pk>/', delete_service, name='delete_service'),
    path('detail/<int:pk>/', service_detail, name='service_detail'),
    path('search/', search_services, name='search_services'),
    #Su dung dich vu
    path('usage/', usage_list, name='usage_list'),
    path('usage/edit/<int:pk>/', edit_usage, name='edit_usage'),
    path('usage/delete/<int:pk>/', delete_usage, name='delete_usage'),
    path('usage/search/', search_usages, name='search_usages'),
    path('usage/export', export_usage_excel, name='export_usage_excel'),
    path('export', export_service_excel, name='export_service_excel'),
    
]