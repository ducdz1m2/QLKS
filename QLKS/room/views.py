from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

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
    with connection.cursor() as cursor:
        cursor.execute("SELECT soPhong, TrangThai, MaLoai_id FROM room_phong WHERE MaPhong = %s", [MaPhong])
        room = cursor.fetchone()

    if not room:  
        messages.error(request, "Phòng không tồn tại!")
        return redirect('room_list')

    # Chuyển đổi số phòng về số nguyên
    soPhong = int(room[0]) if room[0] and room[0].isdigit() else None
    room_dict = {'MaPhong': MaPhong, 'soPhong': soPhong, 'TrangThai': room[1], 'MaLoai_id': room[2]}
    
    loai_phongs = get_all_roomtypes()

    if request.method == 'POST':
        soPhong = request.POST.get('so_phong', '').strip()
        
        # Kiểm tra số phòng hợp lệ
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

    return render(request, 'room/edit_room.html', {'room': room_dict, 'loai_phongs': loai_phongs})

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

