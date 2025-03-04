from django.urls import path
from .views import service_list, add_service, edit_service, delete_service

urlpatterns = [
    path('', service_list, name='service_list'),
    path('add/', add_service, name='add_service'),
    path('edit/<int:pk>/', edit_service, name='edit_service'),
    path('delete/<int:pk>/', delete_service, name='delete_service'),
]