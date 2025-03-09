from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def home(request):
    user = request.user
    if user.is_superuser or user.is_staff:
        return render(request, 'base.html')  # Ưu tiên xử lý admin trước

    if user.is_khachhang():
        return redirect('customer_home')
    elif user.is_nhanvien():
        return redirect('redirect_home')
    
    return render(request, 'base.html')  # fallback nếu không match gì

