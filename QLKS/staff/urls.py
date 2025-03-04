from django.urls import path
from .views import staff_list

urlpatterns = [
    path('', staff_list, name='staff_list')
]