
from django.shortcuts import render
from .models import HoaDon
from django.db import connection


def get_available_invoices():
    with connection.cursor() as cursor:
        cursor.callproc('GetALLInvoices')
        columns = [col[0] for col in cursor.description]  # Lấy tên cột
        return [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert tuple -> dict


def invoices_list(request):
    invoice = get_available_invoices()
    return render(request, 'invoices/invoices_list.html', {'invoices': invoice})
