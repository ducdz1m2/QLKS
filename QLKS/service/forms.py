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
