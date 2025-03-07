from django.shortcuts import render


def home(request):
    return render(request, 'base.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    if request.user.role == 'nhanvien':
        return render(request, 'staff/dashboard.html')  # Giao diện nhân viên
    return render(request, 'customer/dashboard.html')  # Giao diện khách hàng
