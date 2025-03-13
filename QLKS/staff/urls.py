from django.urls import path
from .views import *

urlpatterns = [
    path('', staff_list, name='staff_list'),
    path('home/', staff_home, name='staff_home'),
    path('add/', add_staff, name='add_staff'),
    path('delete/<int:MaNhanVien>/', delete_staff, name='delete_staff'),
    path('edit/<int:MaNhanVien>/', edit_staff, name='edit_staff'),
    path('<int:MaNhanVien>/', view_staff_detail, name='view_staff_detail'),
    path('search/', search_staff, name='search_staff'),
    
    path('receptionist/', receptionist_home, name='receptionist_home'),
    path('export/', export_staff_excel, name='export_staff_excel'),
    path('accept/<int:MaSuDung>', accept, name='accept'),
    path('done/<int:MaSuDung>', done, name='done'),
]
