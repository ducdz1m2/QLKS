from django.urls import path
from .views import *   # Import đúng module views

urlpatterns = [
    path('', customer_list, name='customer_list'),
    path('home/', customer_rentroom, name='customer_rentroom'), # Danh sách của khách hàng
    path('detail/', detail_customer, name='detail_customer'),  # Chỉ hiển thị thông tin của chính họ
    path('search/', search_customer, name='search_customer'), # Tìm kiếm Customer
    # path('add/', add_customer_view, name='add_customer'),
    path('edit/<int:MaKhachHang>', edit_customer, name='edit_customer'),
    path('delete/<int:MaKhachHang>', delete_customer, name='delete_customer'),
    path('detail/<int:MaKhachHang>', detail_customer, name='detail_customer'),
    path('export/', export_customer_excel, name='export_customer_excel'),
    path('rentrooms/', customer_rentroom, name='customer_rentroom'),    
    path('request/<int:MaThue>/', request_service, name='request_service'),  # Yêu cầu dịch vụ
    path('comfirm_request/', comfirm_request, name='comfirm_request'),  # Xác nhận dịch vụ
    path('service_order/', service_order, name='service_order'),  # Xác nhận dịch vụ
]



# from django.urls import path
# from .views import *

# urlpatterns = [
    
# ]