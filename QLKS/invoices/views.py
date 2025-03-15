from django.shortcuts import render, redirect
from .models import *
from django.db import connection
from django.contrib import messages
from .models import HoaDon
from accounts.decorators import phongban_required
from django.contrib.auth.decorators import login_required
import openpyxl
from openpyxl.styles import NamedStyle
from django.http import HttpResponse
from django.utils.timezone import now
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse

def export_invoice_pdf(request, MaHoaDon):
    invoice = get_invoices(MaHoaDon)
    services = get_all_services(invoice['MaThue_id'])

    html_string = render_to_string("invoices/detail_invoices_pdf.html", {
        'invoice': invoice,
        'services': services
    })

    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="invoice.pdf"'
    return response

def export_invoices_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active

    # Tiêu đề sheet
    timestamp = now().strftime('%Y-%m-%d_%H-%M-%S')
    ws.title = "Danh sách hóa đơn"

    # Ghi dòng tiêu đề
    ws.append([
        'Mã hóa đơn', 'Tên khách hàng', 'Số phòng','Địa chỉ', 'Số điện thoại', 'Ngày lập', 'Tổng tiền', 'Trạng thái'
    ])

    # Lấy dữ liệu
    invoices = get_all_invoices()
    
    for row in invoices:
        ws.append([
            row.get('MaHoaDon', ''),
            row.get('TenKhachHang', ''),
            row.get('SoPhong', ''),
            row.get('DiaChi', ''),
            row.get('SoDienThoai', ''),
            row.get('NgayLapHoaDon', '').strftime('%d/%m/%Y'),
            row.get('TongTien', ''),
            row.get('TrangThai', '')
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=hoadon_{timestamp}.xlsx'

    wb.save(response)
    return response


def get_all_customerrentroom():
    with connection.cursor() as cursor:
        cursor.callproc('GetAllIdCustomerRentRoom')
        row = cursor.fetchall()
        row = [item[0] for item in row]
        return row
    
def get_all_services(maThuePhong):
    with connection.cursor() as cursor:
        cursor.callproc('GetServiceByRentRoom', [maThuePhong])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    

@login_required
def detail_invoices(request, MaHoaDon):
    invoice = get_invoices(MaHoaDon)
    if not invoice:
        return render(request, 'invoices/detail_invoices.html', {'error': 'Không tìm thấy hóa đơn'})

    services = get_all_services(invoice['MaThue_id'])
    uri = {
        'previous': request.META.get('HTTP_REFERER', '/invoices/')
    }

    return render(request, 'invoices/detail_invoices.html', {'invoice': invoice, 'services': services, 'uri': uri})

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

    rentrooms= get_all_customerrentroom()
    
    return render(request, 'invoices/add_invoices.html', {'rentrooms': rentrooms})

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

    rentrooms= get_all_customerrentroom()
    return render(request, 'invoices/edit_invoices.html', {'invoices' : invoice, 'rentrooms': rentrooms})

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

    rooms = get_all_rooms()

    print(invoice)
    return render(request, 'invoices/invoices_list.html', {'invoices': invoice, 'rooms': rooms})

# tìm kiếm hóa đơn
@login_required
@phongban_required(allowed_departments=['admin', 'receptionist'])
def search_invoices(request):
    MaHoaDon = request.GET.get('MaHoaDon', '').strip()
    TenKhachHang = request.GET.get('TenKhachHang', '').strip()
    DiaChi = request.GET.get('DiaChi', '').strip()
    SoDienThoai = request.GET.get('SoDienThoai', '').strip()
    SoPhong = request.GET.get('SoPhong', '').strip()
    NgayLapHoaDon = request.GET.get('NgayLapHoaDon', '').strip()
    TrangThai = request.GET.get('TrangThai', '').strip()
    sap_xep = request.GET.get('sap_xep', '').strip()

   

    MaHoaDon = MaHoaDon if MaHoaDon else None
    TenKhachHang = TenKhachHang if TenKhachHang else None
    DiaChi = DiaChi if DiaChi else None
    SoDienThoai = SoDienThoai if SoDienThoai else None
    SoPhong = SoPhong if SoPhong else None
    NgayLapHoaDon = NgayLapHoaDon if NgayLapHoaDon else None
    TrangThai = TrangThai if TrangThai else None
    sap_xep = sap_xep if sap_xep else None
   

    # with connection.cursor() as cursor:
    #     cursor.callproc('SearchInvoices', [MaHoaDon, TenKhachHang, DiaChi, SoDienThoai, SoPhong, NgayLapHoaDon, TrangThai])
    #     columns = [col[0] for col in cursor.description]
    #     invoice = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    with connection.cursor() as cursor:
        cursor.callproc('SearchInvoicesOrderBy', [MaHoaDon, TenKhachHang, DiaChi, SoDienThoai, SoPhong, NgayLapHoaDon, TrangThai, sap_xep])
        columns = [col[0] for col in cursor.description]
        invoice = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    rooms = get_all_rooms()

    print(rooms)
    return render(request, 'invoices/invoices_list.html', {'invoices': invoice, 'rooms': rooms})

def get_all_rooms():
    with connection.cursor() as cursor:
        cursor.callproc('GetAllRooms')
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def pay(request, MaHoaDon):
    with connection.cursor() as cursor:
        cursor.callproc('ThanhToanHoaDon', [MaHoaDon])
        messages.success(request, "Thanh toán hóa đơn thành công")
        return redirect('invoices_list')
