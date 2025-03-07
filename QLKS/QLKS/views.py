from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def home(request):
    if request.user.is_authenticated:
        if request.user.is_khachhang():
            return redirect('customer_home')
        elif request.user.is_nhanvien():
            return redirect('staff_home')
        elif request.user.is_staff or request.user.is_superuser:  
            return render(request, 'base.html')  # Staff hoặc admin vào base.html
    return render(request, 'base.html')
