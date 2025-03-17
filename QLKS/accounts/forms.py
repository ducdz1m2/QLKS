from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser
from staff.models import NhanVien
from customer.models import KhachHang
from room.models import Phong  

class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        # ('nhanvien', 'Nhân viên'),
        ('khachhang', 'Khách hàng'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select'
    }))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control mb-2',
                'placeholder': field.label,
                'style': 'min-height:45px'
            })


class StaffForm(forms.ModelForm):
    class Meta:
        model = NhanVien
        fields = ['HoTen', 'NgaySinh', 'SoDienThoai', 'MaPhongBan']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control mb-2',
                'placeholder': field.label,
                'style': 'min-height:45px'
            })


class CustomerForm(forms.ModelForm):
    class Meta:
        model = KhachHang
        fields = ['TenKhachHang', 'SoDienThoai', 'DiaChi']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control mb-2',
                'placeholder': field.label,
                'style': 'min-height:45px'
            })


class CustomerRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control mb-2',
                'placeholder': field.label,
                'style': 'min-height:45px'
            })
