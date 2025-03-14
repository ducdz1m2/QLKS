from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from .forms import DichVuForm
from staff.views import get_all_phongban
import openpyxl
from django.http import HttpResponse
from django.utils.timezone import now

def export_service_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active

    timestamp = now().strftime('%Y-%m-%d_%H-%M-%S')
    ws.title = "Danh sách dịch vụ"

    # Ghi dòng tiêu đề
    ws.append([
        'Mã dịch vụ', 'Tên dịch vụ', 'Giá dịch vụ', 'Tên phòng ban', 'Trạng thái'
    ])

    # Lấy dữ liệu
    service_list = get_all_services()
    
    for sv in service_list:
        ws.append([
            sv['MaDichVu'],
            sv['TenDichVu'],
            sv['GiaDichVu'],
            sv['TenPhongBan'],
            sv['TrangThai'],
        ])

    # Tạo file response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=dich_vu_{timestamp}.xlsx'

    wb.save(response)
    return response

def export_usage_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active

    # Tiêu đề sheet
    timestamp = now().strftime('%Y-%m-%d_%H-%M-%S')
    ws.title = "Danh sách sử dụng dịch vụ"

    # Ghi dòng tiêu đề
    ws.append([
        'Mã sử dụng', 'Tên khách hàng', 'Số phòng', 'Tên dịch vụ', 'Giá dịch vụ', 'Ngày sử dụng',  'Trạng thái'
    ])

    # Lấy dữ liệu
    usage_list = get_all_usages()

    # Ghi dữ liệu từng dòng
    for row in usage_list:
        ws.append([
            row.get('MaSuDung', ''),
            row.get('TenKhachHang', ''),
            row.get('SoPhong', ''),
            row.get('TenDichVu', ''),
            row.get('GiaDichVu', 0),
            row.get('NgaySuDung', '').strftime('%d-%m-%Y'),
            row.get('TrangThai', ''),
        ])

    # Tạo file response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=su_dung_dich_vu_{timestamp}.xlsx'

    wb.save(response)
    return response


#Dich vu
def service_list(request):
    services = get_all_services()
    phongbans = get_all_phongban()
    print(services)
    return render(request, 'service/service_list.html', {'services': services, 'phongbans': phongbans})

def get_service(pk):
    with connection.cursor() as cursor:
        cursor.callproc('GetService', [pk])
        columns = [col[0] for col in cursor.description]
        result = cursor.fetchone()
        return dict(zip(columns, result)) if result else None

def get_all_services():
    with connection.cursor() as cursor:
        cursor.callproc('GetAllService')
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
def add_service(request):
    if request.method == 'POST':
        form = DichVuForm(request.POST)
        if form.is_valid():
            TenDichVu = form.cleaned_data['TenDichVu']
            GiaDichVu = form.cleaned_data['GiaDichVu']
            PhongBan_id = form.cleaned_data['PhongBan'].MaPhongBan  # Lấy khóa chính

            with connection.cursor() as cursor:
                cursor.callproc('AddService', [TenDichVu, GiaDichVu, PhongBan_id])
            messages.success(request, "Thêm dịch vụ thành công!")
            return redirect('service_list')
    else:
        form = DichVuForm()
    return render(request, 'service/add_service.html', {'form': form})

def edit_service(request, pk):
    service = get_service(pk)
    print(service)
    if not service:
        messages.error(request, "Dịch vụ không tồn tại.")
        return redirect('service_list')

    if request.method == 'POST':
        form = DichVuForm(request.POST)
        if form.is_valid():
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('UpdateService', [
                        pk,
                        form.cleaned_data['TenDichVu'],
                        form.cleaned_data['GiaDichVu'],
                        form.cleaned_data['PhongBan'].MaPhongBan  # Trường này là ForeignKey trong Form
                    ])
                messages.success(request, "Cập nhật dịch vụ thành công!")
                return redirect('service_list')
            except Exception as e:
                messages.error(request, f"Lỗi cập nhật: {str(e)}")
    else:
        form = DichVuForm(initial={
            'TenDichVu': service.get('TenDichVu'),
            'GiaDichVu': service.get('GiaDichVu'),
            'PhongBan': service.get('PhongBan_id')
        })

    return render(request, 'service/edit_service.html', {'form': form})


def delete_service(request, pk):
    service = get_service(pk)
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.callproc('DeleteService', [pk])
        messages.success(request, "Xóa dịch vụ thành công!")
        return redirect('service_list')
    return render(request, 'service/delete_service.html', {'service': service})

def service_detail(request, pk):
    service = get_service(pk)
    print(service)
    if not service:
        messages.error(request, "Dịch vụ không tồn tại!")
        return redirect('service_list')
    return render(request, 'service/detail_service.html', {'service': service})

def search_services(request):
    id = request.GET.get('id') or None
    name = request.GET.get('name') or None
    price = request.GET.get('price') or None
    status = request.GET.get('status') or None
    min_price = request.GET.get('min') or None
    max_price = request.GET.get('max') or None
    phongban_id = request.GET.get('phongban') or None

    services = []
    phongbans = get_all_phongban()
    phongban_dict = {pb['MaPhongBan']: pb['TenPhongBan'] for pb in phongbans}

    with connection.cursor() as cursor:
        cursor.callproc('SearchServices', [id, name, phongban_id, status, price ,min_price, max_price])
        results = cursor.fetchall()
        while cursor.nextset():
            pass

        for row in results:
            services.append({
                'MaDichVu': row[0],
                'TenDichVu': row[1],
                'GiaDichVu': row[2],
                'TenPhongBan': phongban_dict.get(row[3], 'Không rõ'),
                'TrangThai': row[4],
            })

    return render(request, 'service/service_list.html', {
        'services': services,
        'phongbans': phongbans,
    })


#Su dung dich vu
def usage_list(request):
    usages = get_all_usages()
    return render(request, 'usage/usage_list.html', {'usages': usages})

def usage_detail(request, pk):
    usage = get_usage(pk)
    if not usage:
        messages.error(request, "Không tìm thấy dữ liệu sử dụng dịch vụ!")
        return redirect('usage_list')
    return render(request, 'usage/detail_usage.html', {'usage': usage})

def get_usage(pk):
    with connection.cursor() as cursor:
        cursor.callproc('GetUsage', [pk])
        columns = [col[0] for col in cursor.description]
        result = cursor.fetchone()
        return dict(zip(columns, result)) if result else None

def get_all_usages():
    with connection.cursor() as cursor:
        cursor.callproc('GetAllUsage')
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def edit_usage(request, pk):
    usage = get_usage(pk)
    if not usage:
        return redirect('usage_list')
    if request.method == 'POST':
            MaDichVu = request.POST.get('MaDichVu', '').strip()
            NgaySuDung = request.POST.get('NgaySuDung', '').strip()
            TrangThai = request.POST.get('TrangThai', '').strip()
            with connection.cursor() as cursor:
                cursor.callproc('UpdateUsage', [pk, MaDichVu, NgaySuDung, TrangThai])
            messages.success(request, "Cập nhật sử dụng dịch vụ thành công!")
            return redirect('usage_list')
    else:
        services = get_all_services()
        return render(request, 'usage/edit_usage.html', {'usage': usage, 'services': services})

def delete_usage(request, pk):
    usage = get_usage(pk)
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.callproc('DeleteUsage', [pk])
        messages.success(request, "Xóa sử dụng dịch vụ thành công!")
        return redirect('usage_list')
    return render(request, 'usage/delete_usage.html', {'usage': usage})

def search_usages(request):
    MaSuDung = request.GET.get('MaSuDung') or None
    TenKhachHang = request.GET.get('TenKhachHang') or None
    GiaDichVu = request.GET.get('GiaDichVu') or None
    NgaySuDung = request.GET.get('NgaySuDung') or None
    SoPhong = request.GET.get('SoPhong') or None
    TenDichVu = request.GET.get('TenDichVu') or None
    TrangThai = request.GET.get('TrangThai') or None

    with connection.cursor() as cursor:
        cursor.callproc('SearchUsages', [MaSuDung, TenKhachHang, GiaDichVu, NgaySuDung, SoPhong, TenDichVu, TrangThai])
        columns = [col[0] for col in cursor.description]
        invoice = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    rooms = get_all_rooms()
    services = get_all_services()

    return render(request, 'usage/usage_list.html', {
        'usages': invoice,
        'rooms': rooms,
        'services': services,
    })

def get_all_rooms():
    with connection.cursor() as cursor:
        cursor.callproc('GetAllRooms')
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]