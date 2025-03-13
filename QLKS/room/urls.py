from django.urls import path
from .views import *
from customer.views import add_customer_view
urlpatterns = [
    path('', room_list, name='room_list'),
    path('add/', add_room, name='add_room'),
    path('delete/<int:MaPhong>', delete_room, name='delete_room'),
    path('edit/<int:MaPhong>', edit_room, name='edit_room'),
    path('<int:MaPhong>', view_room_detail, name='view_room_detail'),
    path('search/', search_rooms, name='search_rooms'),
    path('rentroom/<int:MaPhong>', add_customer_view, name='add_customer_view'),
    path('return_room/<int:MaPhong>', return_room, name='return_room'),
    path('report/', export_room_excel, name='export_room_excel'),
    
]
