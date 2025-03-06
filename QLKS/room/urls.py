from django.urls import path
from .views import *

urlpatterns = [
    path('', room_list, name='room_list'),
    path('add/', add_room, name='add_room'),
    path('delete/<int:MaPhong>', delete_room, name='delete_room'),
    path('edit/<int:MaPhong>', edit_room, name='edit_room'),
    path('<int:MaPhong>', view_room_detail, name='view_room_detail'),
    path('search/', search_rooms, name='search_rooms'),
]
