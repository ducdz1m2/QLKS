from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

@login_required(login_url='/accounts/login/')
def home(request):
    user = request.user
    if user.is_superuser or user.is_staff:
        return render(request, 'base.html')  # Ưu tiên xử lý admin trước

    if user.is_khachhang():
        return redirect('customer_rentroom')
    elif user.is_nhanvien():
        return redirect('redirect_home')
    
    return render(request, 'base.html')  # fallback nếu không match gì

# đăng nhập
def login_view(request):
    form = AuthenticationForm(request, data = request.POST)

    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        else:
            print(form.errors)  # Debug lỗi

    return render(request, "login.html", {"form": form})        
