from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from accounts.decorators import khachhang_required
from django.contrib import messages
from accounts.forms import CustomerRegisterForm, CustomerForm
from django.contrib.auth import login
from service.views import get_all_services
from room.views import get_room_detail
from accounts.forms import RegisterForm, CustomerForm

def add_customer_view(request, MaPhong):
    room = get_room_detail(MaPhong)
    customers = get_all_customers()

    if request.method == 'POST':
        chon_khach_hang = request.POST.get('chon_khach_hang')
        ma_phong = request.POST.get('ma_phong')
        ngay_thue = request.POST.get('ngay_thue')
        ngay_nhan = request.POST.get('ngay_nhan')
        ngay_tra = request.POST.get('ngay_tra')

        if chon_khach_hang == 'cu':
            customer_id = request.POST.get('customer_id')
            if customer_id:
                add_rentroom(ngay_thue, ngay_nhan, ngay_tra, customer_id, ma_phong)
                messages.success(request, "Thuê phòng thành công cho khách hàng đã có tài khoản.")
                return redirect('room_list')
        else:  # khách mới
            user_form = CustomerRegisterForm(request.POST)
            customer_form = CustomerForm(request.POST)
            if user_form.is_valid() and customer_form.is_valid():
                user = user_form.save(commit=False)
                user.role = 'khachhang'
                user.save()

                customer = customer_form.save(commit=False)
                customer.user = user
                customer.save()

                add_rentroom(ngay_thue, ngay_nhan, ngay_tra, customer.id, ma_phong)
                
                messages.success(request, f"Thuê phòng thành công cho khách hàng mới: {customer.user}")
                return redirect('room_list')
    else:
        user_form = CustomerRegisterForm()
        customer_form = CustomerForm()

    return render(request, 'customer/add_customer.html', {
        'user_form': user_form,
        'customer_form': customer_form,
        'room': room,
        'customers': customers,
    })


def add_rentroom(NgayThue, NgayNhan, NgayTra, khach_hang_id, phong_id):
    with connection.cursor() as cursor:
        cursor.callproc("RentRoomByLeTan", [khach_hang_id, phong_id, NgayThue, NgayNhan, NgayTra])
        
def customer_home(request):
    return render(request, 'customer/customer_home.html')


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



# Lấy một khách hàng theo mã 
def get_customer(MaKhachHang):
    with connection.cursor() as cursor:
        cursor.callproc("GetCustomer", [MaKhachHang])
        row = cursor.fetchone()
        columns = [col[0] for col in cursor.description] if cursor.description else []
        return dict(zip(columns, row)) if row else None
    
# Lấy ra tất cả khách hàng
def get_all_customers():
    with connection.cursor() as cursor:
        cursor.callproc("GetAllCustomer")
        columns = [col[0] for col in cursor.description]  # Lấy tên cột
        return [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert tuple -> dict

# Show thông tin 1 khách hàng   
def detail_customer(request, MaKhachHang):  
    customer = get_customer(MaKhachHang) 
    if not customer:
        return render(request, 'customer/detail_customer.html', {'error': 'Không tìm thấy khách hàng'})
    return render(request, 'customer/detail_customer.html', {'customer' : customer})

# Chỉnh sửa thông tin 1 khách hàng
def edit_customer(request, MaKhachHang):
    customer = get_customer(MaKhachHang)    
    
    if request.method == 'POST':
        TenKhachHang = request.POST.get("TenKhachHang")
        DiaChi = request.POST.get("DiaChi")
        SoDienThoai = request.POST.get("SoDienThoai")
        with connection.cursor() as cursor:
            cursor.callproc('UpdateCustomer', [MaKhachHang ,TenKhachHang, DiaChi, SoDienThoai])
        messages.success(request, f"Cập nhật khách hàng {TenKhachHang} thành công!")
        return redirect('customer_list')
    
    if not customer:
        return render(request, 'customer/edit_customer.html', {'error': 'Không tìm thấy khách hàng'})
    return render(request, 'customer/edit_customer.html', {'customer' : customer})

# Xóa khách hàng
def delete_customer(request, MaKhachHang):
    customer = get_customer(MaKhachHang)  
    if request.method == 'POST':  
        with connection.cursor() as cursor:
            cursor.callproc('DeleteCustomer', [MaKhachHang])
        messages.success(request, f"Xóa khách hàng {customer.TenKhachHang} thành công!")
    return redirect('customer_list')

# Hiện danh sách khách hàng
def customer_list(request):
    customers = get_all_customers()
    return render(request, 'customer/customer_list.html', {'customers': customers})


# Tìm kiếm customer
def search_customer(request):
    TenKhachHang = request.GET.get('TenKhachHang', '').strip()
    DiaChi = request.GET.get('DiaChi', '').strip()
    SoDienThoai = request.GET.get('SoDienThoai', '').strip()
    with connection.cursor() as cursor:
        cursor.callproc('SearchCustomer', [TenKhachHang, DiaChi,SoDienThoai])
        columns = [col[0] for col in cursor.description]
        customers = [dict(zip(columns, row)) for row in cursor.fetchall()]
    # print(TenKhachHang, DiaChi, SoDienThoai, customers)
    return render(request, 'customer/customer_list.html', {"customers": customers})


# ================ Sử dụng dịch vụ của khách hàng ===================
# Lấy tất cả thông tin thuê phòng
def get_all_rentrooms():
    with connection.cursor() as cursor:
        cursor.callproc("GetAllRentRoom")
        columns = [col[0] for col in cursor.description]  # Lấy tên cột
        return [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert tuple -> dict
 
# Hiện danh sách thông tin thuê phòng        
def customer_rentroom(request):
    # Lấy ra thông tin khách hàng đang đăng nhập
    with connection.cursor() as cursor:
        cursor.callproc('GetCustomerByAccountId', [request.user.id])
        columns = [col[0] for col in cursor.description]
        customer = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
    # Lấy ra phòng của khách hàng đang thuê
    with connection.cursor() as cursor:
        cursor.callproc('GetCustomerRentRoom', [customer[0]['id']])   
        columns = [col[0] for col in cursor.description]
        rentRooms = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(customer[0]['id'])
    return render(request, 'customer_rentroom/customer_rentroom.html', {"rentRooms" : rentRooms})



# Yêu cầu dịch vụ
def request_service(request, MaThue):
    services = get_all_services()
    print(MaThue)
    
    return render(request, 'customer_rentroom/customer_addService.html',
                  {'services' : services,
                   'MaThue' : MaThue})

# Xác nhận dịch vụ
def comfirm_request(request):
    servicesIDs = request.POST.getlist("serviceId")
    MaThue = request.POST.get("MaThue")
    for MaDichVu in servicesIDs:
        with connection.cursor() as cursor:
            cursor.callproc("AddUseServiceByCustomer", [MaDichVu, MaThue])
    messages.success(request, f"Yêu cầu dịch vụ thành công!")
    return customer_rentroom(request)
    
# Danh sách dịch vụ đã yêu cầu
def service_order(request):
    # Lấy ra thông tin khách hàng đang đăng nhập
    with connection.cursor() as cursor:
        cursor.callproc('GetCustomerByAccountId', [request.user.id])
        columns = [col[0] for col in cursor.description]
        
        customer = [dict(zip(columns, row)) for row in cursor.fetchall()]
    with connection.cursor() as cursor:
        cursor.callproc("GetCustomerServiceByRentRoom", [customer[0]['id']])
        columns = [col[0] for col in cursor.description]  
        services = [dict(zip(columns, row)) for row in cursor.fetchall()] 
    return render(request, 'customer_rentroom/customer_serviceOrder.html', {"services" : services})
