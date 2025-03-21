from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import phongban_required
from django.views.decorators.csrf import csrf_exempt
import openpyxl
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def export_staff_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Danh sách nhân viên"

    ws.append(['Mã nhân viên', 'Họ tên', 'Ngày sinh', 'Số điện thoại', 'Phòng ban'])

    staff_list = get_all_staff()
    for nv in staff_list:
        ws.append([
            nv.get('MaNhanVien', ''),
            nv.get('HoTen', ''),
            nv.get('NgaySinh', ''),
            nv.get('SoDienThoai', ''),
            nv.get('TenPhongBan', ''),
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=nhan_vien.xlsx'
    wb.save(response)
    return response

@csrf_exempt
def accept(request, MaSuDung):
    user_id = request.user.id
    MaNhanVien = 0
    with connection.cursor() as cursor:
        cursor.callproc('GetStaffId', [user_id])
        MaNhanVien = cursor.fetchone()[0]
    
    with connection.cursor() as cursor:
        cursor.callproc('AcceptTask', [MaNhanVien, MaSuDung])
    with connection.cursor() as cursor:
        cursor.callproc('UpdateUsage1', [MaSuDung])
    

    with connection.cursor() as cursor:
        cursor.callproc('GetTaskByStaffId', [MaNhanVien])
        staff_task = cursor.fetchone()
        messages.success(request, "Chấp nhận công việc")
        return render(request, 'staff/staff_task.html', {'staff_task': staff_task})


def done(request, MaSuDung):
    user_id = request.user.id
    MaNhanVien = 0
    with connection.cursor() as cursor:
        cursor.callproc('GetStaffId', [user_id])
        MaNhanVien = cursor.fetchone()[0]

    with connection.cursor() as cursor:
        cursor.callproc('DoneTask', [MaNhanVien])
    with connection.cursor() as cursor:
        cursor.callproc('UpdateUsage2', [MaSuDung])
    
    messages.success(request, "Hoàn thành công việc")
    return redirect('/')

def getTask(MaPhongBan):
    with connection.cursor() as cursor:
        cursor.callproc('GetStaffTask', [MaPhongBan])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

@login_required
def staff_home(request):
    user_id = request.user.id

    with connection.cursor() as cursor:
        cursor.callproc('GetStaffId', [user_id])
        result1 = cursor.fetchone()
    MaNhanVien = result1[0] if result1 else 0

    with connection.cursor() as cursor:
        cursor.callproc('GetPhongBanByStaffId', [MaNhanVien])
        result2 = cursor.fetchone()
    PhongBan = result2  

    with connection.cursor() as cursor:
        cursor.callproc('GetTaskByStaffId', [MaNhanVien])
        staff_task = cursor.fetchone()
    
    if staff_task:
        return render(request, 'staff/staff_task.html', {
            'staff_task': staff_task,
            'TenPhongBan': PhongBan[1]
        })
    else:
        tasks = getTask(PhongBan[0])  
        return render(request, 'staff/staff_home.html', {
            'tasks': tasks,
            'TenPhongBan': PhongBan[1]
        })

@login_required
@phongban_required(allowed_departments=['receptionist'])
def receptionist_home(request):
    return render(request, 'staff/receptionist_home.html')



def get_phongban_by_id(MaPhongBan):
     with connection.cursor() as cursor:
        cursor.callproc('GetPhongBanById', [MaPhongBan])
        
        return cursor.fetchone()
    

# lay phòng ban
def get_all_phongban():
    with connection.cursor() as cursor:
        cursor.callproc('GetAllPhongBan')
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
# Lấy danh sách nhân viên
def get_all_staff():
    with connection.cursor() as cursor:
        cursor.callproc('GetAllStaff')
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

# Xem chi tiết nhân viên
def get_staff_detail(MaNhanVien):
    with connection.cursor() as cursor:
        cursor.callproc('GetDetailStaff', [MaNhanVien])
        row = cursor.fetchone()
        columns = [col[0] for col in cursor.description] if cursor.description else []
        return dict(zip(columns, row)) if row else None

def view_staff_detail(request, MaNhanVien):
    staff = get_staff_detail(MaNhanVien)
    
    if not staff:
        return render(request, 'staff/detail_staff.html', {'error': 'Không tìm thấy nhân viên'})
    phongban = list(get_phongban_by_id(staff['MaPhongBan_id']))[0]
    # phongban = temp['tenphongban']
    print(phongban)
    return render(request, 'staff/detail_staff.html', {'staff': staff, 'phongban': phongban})

# Thêm nhân viên
def add_staff(request):
    if request.method == 'POST':
        HoTen = request.POST['ho_ten']
        NgaySinh = request.POST['ngay_sinh']
        SoDienThoai = request.POST['so_dien_thoai']
        MaPhongBan_id = request.POST['ma_phong_ban_id']

        with connection.cursor() as cursor:
            cursor.callproc('AddStaff', [HoTen, NgaySinh, SoDienThoai, MaPhongBan_id])

        messages.success(request, f"Thêm nhân viên {HoTen} thành công!")
        return redirect('staff_list')
    phong_bans = get_all_phongban()
    return render(request, 'staff/add_staff.html', {'phong_bans': phong_bans})

# Chỉnh sửa nhân viên
def edit_staff(request, MaNhanVien):
    staff = get_staff_detail(MaNhanVien)

    if not staff:
        messages.error(request, "Nhân viên không tồn tại!")
        return redirect('staff_list')

    if request.method == 'POST':
        HoTen = request.POST.get('ho_ten', '').strip()
        NgaySinh = request.POST.get('ngay_sinh')
        SoDienThoai = request.POST.get('so_dien_thoai')
        MaPhongBan_id = request.POST.get('ma_phong_ban_id')
        print(NgaySinh)
        with connection.cursor() as cursor:
            cursor.callproc('UpdateStaff', [MaNhanVien, HoTen, NgaySinh, SoDienThoai, MaPhongBan_id])

        messages.success(request, f"Cập nhật nhân viên {HoTen} thành công!")
        return redirect('staff_list')
    phong_bans = get_all_phongban()
    return render(request, 'staff/edit_staff.html', {'staff': staff, 'phong_bans': phong_bans})

# Xóa nhân viên
def delete_staff(request, MaNhanVien):
    if request.method == 'POST':
        HoTen = get_staff_detail(MaNhanVien)['HoTen']

        with connection.cursor() as cursor:
            cursor.callproc('DeleteStaff', [MaNhanVien])

        messages.success(request, f"Xóa nhân viên {HoTen} thành công!")
    return redirect('staff_list')

# Tìm kiếm nhân viên
def search_staff(request):
    ho_ten = request.GET.get('ho_ten', '').strip()
    so_dien_thoai = request.GET.get('so_dien_thoai', '').strip()
    ma_phong_ban_id = request.GET.get('ma_phong_ban_id', '').strip()

    ho_ten = ho_ten if ho_ten else None
    so_dien_thoai = so_dien_thoai if so_dien_thoai else None
    ma_phong_ban_id = ma_phong_ban_id if ma_phong_ban_id else None

    with connection.cursor() as cursor:
        cursor.callproc('SearchStaff', [ho_ten, so_dien_thoai, ma_phong_ban_id])
        columns = [col[0] for col in cursor.description]
        staffs = [dict(zip(columns, row)) for row in cursor.fetchall()]
    phong_bans = get_all_phongban()
    return render(request, 'staff/staff_list.html', {'staffs': staffs, 'phong_bans':phong_bans})

# Danh sách nhân viên
def staff_list(request):
    staffs = get_all_staff()
    phong_bans = get_all_phongban()
    return render(request, 'staff/staff_list.html', {'staffs': staffs, 'phong_bans':phong_bans})
