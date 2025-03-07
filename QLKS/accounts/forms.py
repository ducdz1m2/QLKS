from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser
from staff.models import NhanVien
from customer.models import KhachHang

class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        ('nhanvien', 'Nhân viên'),
        ('khachhang', 'Khách hàng'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select())

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

class StaffForm(forms.ModelForm):
    class Meta:
        model = NhanVien
        fields = ['HoTen', 'NgaySinh', 'SoDienThoai', 'MaPhongBan']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = KhachHang
        fields = ['TenKhachHang', 'SoDienThoai', 'DiaChi']
