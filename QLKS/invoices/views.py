from django.shortcuts import render, redirect
from .models import *
from django.db import connection
from django.contrib import messages
from .models import HoaDon
from accounts.decorators import phongban_required
from django.contrib.auth.decorators import login_required

def get_all_useservice():
    with connection.cursor() as cursor:
        cursor.callproc('GetAllMaUseService')
        row = cursor.fetchall()
        row = [item[0] for item in row]
        return row

def get_invoices_detail(MaHoaDon):
    with connection.cursor() as cursor:
        cursor.callproc('GetDetailInvoices', [MaHoaDon])
        row = cursor.fetchone()
        columns = [col[0] for col in cursor.description] if cursor.description else []
        return dict(zip(columns, row)) if row else None
@login_required
@phongban_required(allowed_departments=['admin', 'receptionist'])
def detail_invoices(request, MaHoaDon):
    invoice = get_invoices(MaHoaDon)
    if not invoice:
        return render(request, 'invoices/detail_invoices.html', {'error': 'Không tìm thấy hóa đơn'})
    return render(request, 'invoices/detail_invoices.html', {'invoices': invoice})

@login_required
@phongban_required(allowed_departments=['admin', 'receptionist'])
def add_invoices(request):
    print(request)
    if request.method == 'POST':
        
        NgayLapHoaDon = request.POST['NgayLapHoaDon']
        TongTien = request.POST['TongTien']
        MaThue_id = request.POST['MaThue_id']
        print(NgayLapHoaDon, TongTien)
        with connection.cursor() as cursor:
            cursor.callproc('AddInvoices', [NgayLapHoaDon, TongTien, MaThue_id])
            
        messages.success(request, f"Thêm hóa đơn thành công!")

    useservices= get_all_useservice()
    
    return render(request, 'invoices/add_invoices.html', {'useservices': useservices})

# Lấy một hóa đơn theo mã 
def get_invoices(MaHoaDon):
    with connection.cursor() as cursor:
        cursor.callproc("GetInvoices", [MaHoaDon])
        row = cursor.fetchone()
        columns = [col[0] for col in cursor.description] if cursor.description else []
        return dict(zip(columns, row)) if row else None
    
@login_required
@phongban_required(allowed_departments=['admin', 'receptionist'])
def edit_invoices(request, MaHoaDon):
    invoice = get_invoices(MaHoaDon)    
    
    if request.method == 'POST':
        NgayLapHoaDon = request.POST.get("NgayLapHoaDon")
        TongTien = request.POST.get("TongTien")
        MaThue_id = request.POST.get("MaThue_id")
        with connection.cursor() as cursor:
            cursor.callproc('UpdateInvoices', [MaHoaDon ,NgayLapHoaDon, MaThue_id, TongTien])
        messages.success(request, f"Cập nhật hóa đơn {MaHoaDon} thành công!")
        return redirect('invoices_list')
    
    if not invoice:
        return render(request, 'invoices/edit_invoices.html', {'error': 'Không tìm thấy hóa đơn'})
    
    useservices= get_all_useservice()
    return render(request, 'invoices/edit_invoices.html', {'invoices' : invoice, 'useservices': useservices})

# Xóa hóa đơn
def delete_invoices(request, MaHoaDon):
    

    if request.method == 'POST':  
        with connection.cursor() as cursor:
            cursor.callproc('DeleteInvoices', [MaHoaDon])
        messages.success(request, f"Xóa hóa đơn {MaHoaDon} thành công!")
    return redirect('invoices_list')


def get_all_invoices():
    with connection.cursor() as cursor:
        cursor.callproc('GetAllInvoices')
        columns = [col[0] for col in cursor.description]  # Lấy tên cột
        return [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert tuple -> dict
def get_all_invoicestypes():
    with connection.cursor() as cursor:
        cursor.callproc('GetAllInvoicesType')
        columns = [col[0] for col in cursor.description]  # Lấy tên cột
        return [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert tuple -> dict
@login_required
@phongban_required(allowed_departments=['admin', 'receptionist'])
def invoices_list(request):
    invoice= get_all_invoices()
    invoices_types = []
    temp = get_all_invoicestypes()
    for item in temp:
        invoices_types.append(item['phong_id'])
    print(invoices_types)
    return render(request, 'invoices/invoices_list.html', {'invoices': invoice, 'invoices_types': invoices_types})

# tìm kiếm hóa đơn
@login_required
@phongban_required(allowed_departments=['admin', 'receptionist'])
def search_invoices(request):
    MaHoaDon = request.GET.get('MaHoaDon', '').strip()
    NgayLapHoaDon = request.GET.get('NgayLapHoaDon', '').strip()
    TongTien = request.GET.get('TongTien', '').strip()
    MaThue_id = request.GET.get('MaThue_id', '').strip()
   

    MaHoaDon = MaHoaDon if MaHoaDon else None
    NgayLapHoaDon = NgayLapHoaDon if NgayLapHoaDon else None
    TongTien = TongTien if TongTien else None
    MaThue_id = MaThue_id if MaThue_id else None
   

    with connection.cursor() as cursor:
        cursor.callproc('SearchInvoices', [MaHoaDon, NgayLapHoaDon,TongTien, MaThue_id])
        columns = [col[0] for col in cursor.description]
        invoice = [dict(zip(columns, row)) for row in cursor.fetchall()]
    invoices_types = []
    temp = get_all_invoicestypes()
    for item in temp:
        invoices_types.append(item['MaThue'])

    print(invoices_types)
    return render(request, 'invoices/invoices_list.html', {'invoices': invoice, 'invoices_types': invoices_types})