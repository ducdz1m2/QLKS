from django import forms
from .models import DichVu

#Dich vu
class DichVuForm(forms.ModelForm):
    class Meta:
        model = DichVu
        fields = ['TenDichVu', 'GiaDichVu', 'PhongBan']
        widgets = {
            'TenDichVu': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tên dịch vụ'
            }),
            'GiaDichVu': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập giá dịch vụ'
            }),
            'PhongBan': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


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