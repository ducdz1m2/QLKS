from django.shortcuts import render
from .models import Phong
from django.db import connection


def get_available_rooms():
    with connection.cursor() as cursor:
        cursor.callproc('GetAllRooms')
        columns = [col[0] for col in cursor.description]  # Lấy tên cột
        return [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert tuple -> dict


def room_list(request):
    rooms = get_available_rooms()
    print(rooms)
    return render(request, 'room/room_list.html', {'rooms': rooms})

