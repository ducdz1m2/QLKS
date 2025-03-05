from django import forms
from .models import DichVu

#Dich vu
class DichVuForm(forms.Form):
    TenDichVu = forms.CharField(
        label="Tên Dịch Vụ", 
        max_length=100, 
        required=True, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tên dịch vụ'
            }
        )
    )

    GiaDichVu = forms.DecimalField(
        label="Giá Dịch Vụ", 
        max_digits=10, 
        decimal_places=2, 
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nhập giá dịch vụ'
            }
        )
    )

#Su dung dich vu
class SuDungDichVuForm(forms.Form):
    MaThue = forms.IntegerField(
        label="Mã Thuê", 
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nhập mã thuê'
            }
        )
    )

    MaDichVu = forms.IntegerField(
        label="Mã Dịch Vụ", 
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nhập mã dịch vụ'
            }
        )
    )

    SoLuong = forms.IntegerField(
        label="Số Lượng", 
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nhập số lượng'
            }
        )
    )

    NgaySuDung = forms.DateField(
        label="Ngày Sử Dụng", 
        required=True, 
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        )
    )