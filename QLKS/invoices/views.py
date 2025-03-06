from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db import connection
from django.contrib import messages
from .models import HoaDon

from django.db import connection
from django.shortcuts import render

def get_invoices_detail(MaHoaDon):
    with connection.cursor() as cursor:
        cursor.callproc('GetDetailInvoices', [MaHoaDon])
        row = cursor.fetchone()
        columns = [col[0] for col in cursor.description] if cursor.description else []
        return dict(zip(columns, row)) if row else None

def detail_invoices(request, MaHoaDon):
    invoice = get_invoices(MaHoaDon)
    if not invoice:
        return render(request, 'invoices/detail_invoices.html', {'error': 'Không tìm thấy hóa đơn'})
    return render(request, 'invoices/detail_invoices.html', {'invoices': invoice})


def add_invoices(request):
    print(request)
    if request.method == 'POST':
        
        NgayLapHoaDon = request.POST['NgayLapHoaDon']
        TongTien = request.POST['TongTien']
        MaSuDung_id = request.POST['MaSuDung_id']
        print(NgayLapHoaDon, TongTien)
        with connection.cursor() as cursor:
            cursor.callproc('AddInvoices', [NgayLapHoaDon, TongTien, MaSuDung_id])
            
        messages.success(request, f"Thêm hóa đơn thành công!")
    return render(request, 'invoices/add_invoices.html')


# def edit_invoices(request, MaHoaDon):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT NgayLapHoaDon, TongTien, MaSuDung_id FROM invoices_hoadon WHERE MaHoaDon = %s", [MaHoaDon])
#         invoice = cursor.fetchone()

#     if not invoice:  
#         messages.error(request, "Hóa đơn không tồn tại!")
#         return redirect('invoices_list')

#     invoices_dict = {'NgayLapHoaDon': invoice[0], 'TongTien': invoice[1], 'MaSuDung_id': invoice[2]}

#     if request.method == 'POST':
#         NgayLapHoaDon = request.POST.get('ngay_lap_hoa_don')
#         TongTien = request.POST.get('tong_tien')
#         MaSuDung_id = request.POST.get('ma_su_dung_id')

#         with connection.cursor() as cursor:
#             cursor.callproc('UpdateInvoices', [NgayLapHoaDon, TongTien, MaSuDung_id, MaHoaDon])

#         messages.success(request, f"Cập nhật hóa đơn {MaHoaDon} thành công!")
#         return redirect('invoices_list')

#     return render(request, 'invoices/edit_invoices.html', {'invoices': invoices_dict})
# Lấy một hóa đơn theo mã 
def get_invoices(MaHoaDon):
    with connection.cursor() as cursor:
        cursor.callproc("GetInvoices", [MaHoaDon])
        row = cursor.fetchone()
        columns = [col[0] for col in cursor.description] if cursor.description else []
        return dict(zip(columns, row)) if row else None
    

def edit_invoices(request, MaHoaDon):
    invoice = get_invoices(MaHoaDon)    
    
    if request.method == 'POST':
        NgayLapHoaDon = request.POST.get("NgayLapHoaDon")
        TongTien = request.POST.get("TongTien")
        MaSuDung_id = request.POST.get("MaSuDung_id")
        with connection.cursor() as cursor:
            cursor.callproc('UpdateInvoices', [MaHoaDon ,NgayLapHoaDon, TongTien, MaSuDung_id])
        messages.success(request, f"Cập nhật hóa đơn {MaHoaDon} thành công!")
        return redirect('invoices_list')
    
    if not invoice:
        return render(request, 'invoices/edit_invoices.html', {'error': 'Không tìm thấy hóa đơn'})
    return render(request, 'invoices/edit_invoices.html', {'invoices' : invoice})

# Xóa hóa đơn
def delete_invoices(request, MaHoaDon):
    invoice = get_invoices(MaHoaDon)  
    if request.method == 'POST':  
        with connection.cursor() as cursor:
            cursor.callproc('DeleteInvoices', [MaHoaDon])
        messages.success(request, f"Xóa hóa đơn {invoice.MaHoaDon} thành công!")
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

def invoices_list(request):
    invoice= get_all_invoices()
    return render(request, 'invoices/invoices_list.html', {'invoices': invoice})

