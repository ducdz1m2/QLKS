from django.urls import path
from .views import customer_list, rentroom_list

urlpatterns = [
    path('', customer_list, name='customer_list'),
    path('rentroom/', rentroom_list, name='rentroom_list'),
]