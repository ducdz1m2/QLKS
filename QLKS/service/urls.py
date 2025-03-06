from django.urls import path
from .views import service_list, add_service, edit_service, delete_service, service_detail
from .views import usage_list, add_usage, edit_usage, delete_usage

urlpatterns = [
    #Dich vu
    path('', service_list, name='service_list'),
    path('add/', add_service, name='add_service'),
    path('edit/<int:pk>/', edit_service, name='edit_service'),
    path('delete/<int:pk>/', delete_service, name='delete_service'),
    path('detail/<int:pk>/', service_detail, name='service_detail'),
    #Su dung dich vu
    path('usage/', usage_list, name='usage_list'),
    path('usage/add/', add_usage, name='add_usage'),
    path('usage/edit/<int:pk>/', edit_usage, name='edit_usage'),
    path('usage/delete/<int:pk>/', delete_usage, name='delete_usage'),
]