from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages


def get_room_detail(MaPhong):
    with connection.cursor() as cursor:
        cursor.callproc('GetDetailRoom', [MaPhong])
        row = cursor.fetchone()
        columns = [col[0] for col in cursor.description] if cursor.description else []
        return dict(zip(columns, row)) if row else None

def view_room_detail(request, MaPhong):
    room = get_room_detail(MaPhong)
    print(room)
    if not room:
        return render(request, 'room/detail_room.html', {'error': 'Không tìm thấy phòng'})
    return render(request, 'room/detail_room.html', {'room': room})


def add_room(request):
    print(request)
    if request.method == 'POST':
        
        SoPhong = request.POST['so_phong']
        TrangThai = request.POST['trang_thai']
        MaLoai_id = request.POST['ma_loai_id']
        print(SoPhong, TrangThai)
        with connection.cursor() as cursor:
            cursor.callproc('AddRoom', [SoPhong, TrangThai, MaLoai_id])
        messages.success(request, f"Thêm phòng {SoPhong} thành công!")
    return render(request, 'room/add_room.html')

def delete_room(request, MaPhong):
    if request.method == 'POST':  
        
        SoPhong = request.POST['so_phong']
        with connection.cursor() as cursor:
            cursor.callproc('DeleteRoom', [MaPhong])
        messages.success(request, f"Xóa phòng {SoPhong} thành công!")
    return redirect('room_list')

def edit_room(request, MaPhong):
    room = get_room_detail(MaPhong)

    if not room:  
        messages.error(request, "Phòng không tồn tại!")
        return redirect('room_list')
    
    loai_phongs = get_all_roomtypes()

    if request.method == 'POST':
        soPhong = request.POST.get('so_phong', '').strip()
        if not soPhong.isdigit():
            messages.error(request, "Số phòng không hợp lệ!")
            return redirect(f'/room/edit/{MaPhong}')

        soPhong = int(soPhong)  # Ép kiểu về số nguyên
        TrangThai = request.POST.get('trang_thai')
        MaLoai_id = request.POST.get('ma_loai_id')

        with connection.cursor() as cursor:
            cursor.callproc('UpdateRoom', [soPhong, TrangThai, MaLoai_id, MaPhong])

        messages.success(request, f"Cập nhật phòng {soPhong} thành công!")
        return redirect('room_list')

    return render(request, 'room/edit_room.html', {'room': room, 'loai_phongs': loai_phongs})

def get_all_rooms():
    with connection.cursor() as cursor:
        cursor.callproc('GetAllRooms')
        columns = [col[0] for col in cursor.description]  # Lấy tên cột
        return [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert tuple -> dict
def get_all_roomtypes():
    with connection.cursor() as cursor:
        cursor.callproc('GetAllRoomType')
        columns = [col[0] for col in cursor.description]  # Lấy tên cột
        return [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert tuple -> dict

def room_list(request):
    rooms = get_all_rooms()
    print(rooms)
    return render(request, 'room/room_list.html', {'rooms': rooms})

## NEW ###
def search_rooms(request):
    so_phong = request.GET.get('so_phong', '').strip()
    trang_thai = request.GET.get('trang_thai', '').strip()
    ten_loai = request.GET.get('ten_loai', '').strip()  # Lấy TenLoai từ request

    # Xử lý giá trị rỗng -> NULL
    so_phong = so_phong if so_phong else None
    trang_thai = trang_thai if trang_thai else None
    ten_loai = ten_loai if ten_loai else None  # Giữ dạng chuỗi, không cần chuyển kiểu

    with connection.cursor() as cursor:
        cursor.callproc('SearchRooms', [so_phong, trang_thai, ten_loai])
        columns = [col[0] for col in cursor.description]
        rooms = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    room_types = get_all_roomtypes()
    print(rooms)  # Debug kết quả
    return render(request, 'room/room_list.html', {'rooms': rooms, 'room_types': room_types})
