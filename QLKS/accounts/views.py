from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import login
from accounts.forms import RegisterForm, StaffForm, CustomerForm
from accounts.models import CustomUser

def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            
            # Nếu là nhân viên
            if user.role == 'nhanvien':
                staff_form = StaffForm(request.POST)
                if staff_form.is_valid():
                    staff = staff_form.save(commit=False)
                    staff.user = user
                    staff.save()
            
            # Nếu là khách hàng
            elif user.role == 'khachhang':
                customer_form = CustomerForm(request.POST)
                if customer_form.is_valid():
                    customer = customer_form.save(commit=False)
                    customer.user = user
                    customer.save()

            login(request, user)
            return redirect('home')  # Điều hướng về trang chủ

    else:
        user_form = RegisterForm()
        staff_form = StaffForm()
        customer_form = CustomerForm()

    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'staff_form': staff_form,
        'customer_form': customer_form
    })

@csrf_exempt  # Tắt CSRF để logout dễ dàng hơn (có thể bỏ nếu không cần)
def logout_view(request):
    if request.method in ['POST', 'GET']:  # Cho phép cả GET và POST
        logout(request)
        return redirect('/accounts/login/')
    return redirect('/')  # Nếu request không hợp lệ, quay về trang chủ
