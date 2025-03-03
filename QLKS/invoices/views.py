from django.shortcuts import render
from.models import HoaDon
# Create your views here.

def invoices_list(request):
    invoice = HoaDon.objects.all()
    return render(request, 'invoices/invoices_list.html', {'invoices': invoice})