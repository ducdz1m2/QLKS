from django.shortcuts import render
from django.db import connection


def get_all_staff():
    with connection.cursor() as cursor:
        cursor.callproc('GetAllStaff')
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def staff_list(request):
    staffs = get_all_staff()
    return render(request, 'staff/staff_list.html', {'staffs': staffs})