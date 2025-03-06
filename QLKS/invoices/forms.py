from django import forms
from .models import HoaDon

class HoaDonForm(forms.ModelForm):
    class Meta:
        model = HoaDon
        fields = ['MaHoaDon', 'MaSDDV','NgayLapHoaDon','TongTien']