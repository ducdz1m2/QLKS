from django.shortcuts import render
from .models import KhachHang, ThuePhong
from django.db import connection

# Create your views here.
def get_all_customers():
    with connection.cursor() as cursor:
        cursor.callproc("GetAllCustomer")
        columns = [col[0] for col in cursor.description]  # Lấy tên cột
        return [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert tuple -> dict

def customer_list(request):
    customers = get_all_customers()
    return render(request, 'customer/customer_list.html', {'customers': customers})

def get_all_rentrooms():
    with connection.cursor() as cursor:
        cursor.callproc("GetAllRentRoom")
        columns = [col[0] for col in cursor.description]  # Lấy tên cột
        return [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert tuple -> dict
        
def rentroom_list(request):
    rentrooms = get_all_rentrooms()
    print(rentrooms)
    return render(request, 'rentroom/rentroom_list.html', {'rentrooms': rentrooms})