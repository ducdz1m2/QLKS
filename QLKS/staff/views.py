from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

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
