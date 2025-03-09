from django.urls import path
from .views import *   # Import đúng module views

urlpatterns = [
    path('', customer_list, name='customer_list'),
    path('home/', customer_home, name='customer_home'),
    path('detail/', detail_customer, name='detail_customer'),  # Chỉ hiển thị thông tin của chính họ
    path('rentrooms/', rentroom_list, name='rentroom_list'),  # Danh sách phòng có sẵn
    path('request-service/', request_service, name='request_service'),  # Yêu cầu dịch vụ
    path('add/', add_customer_view, name='add_customer'),
    path('edit/<int:MaKhachHang>', edit_customer, name='edit_customer'),
    path('delete/<int:MaKhachHang>', delete_customer, name='delete_customer'),
    path('detail/<int:MaKhachHang>', detail_customer, name='detail_customer'),
]



# from django.urls import path
# from .views import *

# urlpatterns = [
    
# ]