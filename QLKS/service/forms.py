from django import forms
from .models import DichVu

#Dich vu
class DichVuForm(forms.Form):
    TenDichVu = forms.CharField(label="Tên Dịch Vụ", max_length=100, required=True)
    GiaDichVu = forms.DecimalField(
        label="Giá Dịch Vụ", 
        max_digits=10, 
        decimal_places=2, 
        required=False
    )

#Su dung dich vu
class SuDungDichVuForm(forms.Form):
    MaThue = forms.IntegerField(label="Mã Thuê", required=True)
    MaDichVu = forms.IntegerField(label="Mã Dịch Vụ", required=True)
    SoLuong = forms.IntegerField(label="Số Lượng", required=True)
    NgaySuDung = forms.DateField(
        label="Ngày Sử Dụng", 
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )