from django import forms
from .models import DichVu

class DichVuForm(forms.ModelForm):
    class Meta:
        model = DichVu
        fields = ['TenDichVu', 'GiaDichVu']