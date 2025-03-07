from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required
from accounts.decorators import khachhang_required

@login_required
@khachhang_required
def customer_home(request):
    return render(request, 'customer/customer_home.html')

# Lấy thông tin một khách hàng (chỉ lấy của chính họ)
@login_required
@khachhang_required
def detail_customer(request):  
    MaKhachHang = request.user.id  # Lấy ID của user hiện tại  
    with connection.cursor() as cursor:
        cursor.callproc("GetCustomer", [MaKhachHang])
        row = cursor.fetchone()
        columns = [col[0] for col in cursor.description] if cursor.description else []
        customer = dict(zip(columns, row)) if row else None

    if not customer:
        return render(request, 'customer/detail_customer.html', {'error': 'Không tìm thấy thông tin khách hàng'})
    
    return render(request, 'customer/detail_customer.html', {'customer': customer})

# Lấy danh sách phòng & dịch vụ có sẵn
@login_required
@khachhang_required
def rentroom_list(request):
    with connection.cursor() as cursor:
        cursor.callproc("GetAllRentRoom")
        columns = [col[0] for col in cursor.description]  
        rentrooms = [dict(zip(columns, row)) for row in cursor.fetchall()]  

    return render(request, 'customer/rentroom_list.html', {'rentrooms': rentrooms})

# Yêu cầu dịch vụ
@login_required
@khachhang_required
def request_service(request):
    if request.method == 'POST':
        MaKhachHang = request.user.id  
        MaDichVu = request.POST.get('MaDichVu')  
        
        with connection.cursor() as cursor:
            cursor.callproc('RequestService', [MaKhachHang, MaDichVu])
        
        return render(request, 'customer/service_success.html', {'message': 'Yêu cầu dịch vụ thành công!'})

    return render(request, 'customer/request_service.html')











# Thêm khách hàng
# def add_customer(request):
#     if request.method == "POST":
#         TenKhachHang = request.POST['TenKhachHang']
#         DiaChi = request.POST['DiaChi']
#         SoDienThoai = request.POST['SoDienThoai']
#         with connection.cursor() as cursor:
#             cursor.callproc('AddCustomer', [TenKhachHang, DiaChi, SoDienThoai])
#         messages.success(request, f"Thêm khách hàng {TenKhachHang} thành công!")
#     return render(request, 'customer/add_customer.html')

# # Lấy một khách hàng theo mã 
# def get_customer(MaKhachHang):
#     with connection.cursor() as cursor:
#         cursor.callproc("GetCustomer", [MaKhachHang])
#         row = cursor.fetchone()
#         columns = [col[0] for col in cursor.description] if cursor.description else []
#         return dict(zip(columns, row)) if row else None
    
# # Lấy ra tất cả khách hàng
# def get_all_customers():
#     with connection.cursor() as cursor:
#         cursor.callproc("GetAllCustomer")
#         columns = [col[0] for col in cursor.description]  # Lấy tên cột
#         return [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert tuple -> dict

# # Show thông tin 1 khách hàng   
# def detail_customer(request, MaKhachHang):  
#     customer = get_customer(MaKhachHang) 
#     if not customer:
#         return render(request, 'customer/detail_customer.html', {'error': 'Không tìm thấy khách hàng'})
#     return render(request, 'customer/detail_customer.html', {'customer' : customer})

# # Chỉnh sửa thông tin 1 khách hàng
# def edit_customer(request, MaKhachHang):
#     customer = get_customer(MaKhachHang)    
    
#     if request.method == 'POST':
#         TenKhachHang = request.POST.get("TenKhachHang")
#         DiaChi = request.POST.get("DiaChi")
#         SoDienThoai = request.POST.get("SoDienThoai")
#         with connection.cursor() as cursor:
#             cursor.callproc('UpdateCustomer', [MaKhachHang ,TenKhachHang, DiaChi, SoDienThoai])
#         messages.success(request, f"Cập nhật khách hàng {TenKhachHang} thành công!")
#         return redirect('customer_list')
    
#     if not customer:
#         return render(request, 'customer/edit_customer.html', {'error': 'Không tìm thấy khách hàng'})
#     return render(request, 'customer/edit_customer.html', {'customer' : customer})

# # Xóa khách hàng
# def delete_customer(request, MaKhachHang):
#     customer = get_customer(MaKhachHang)  
#     if request.method == 'POST':  
#         with connection.cursor() as cursor:
#             cursor.callproc('DeleteCustomer', [MaKhachHang])
#         messages.success(request, f"Xóa khách hàng {customer.TenKhachHang} thành công!")
#     return redirect('customer_list')

# # Hiện danh sách khách hàng
# def customer_list(request):
#     customers = get_all_customers()
#     return render(request, 'customer/customer_list.html', {'customers': customers})

# # Lấy tất cả thông tin thuê phòng
# def get_all_rentrooms():
#     with connection.cursor() as cursor:
#         cursor.callproc("GetAllRentRoom")
#         columns = [col[0] for col in cursor.description]  # Lấy tên cột
#         return [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert tuple -> dict
 
# # Hiện danh sách thông tin thuê phòng        
# def rentroom_list(request):
#     rentrooms = get_all_rentrooms()
#     print(rentrooms)
#     return render(request, 'rentroom/rentroom_list.html', {'rentrooms': rentrooms})