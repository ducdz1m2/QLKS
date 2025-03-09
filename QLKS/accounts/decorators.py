from django.contrib.auth.decorators import user_passes_test
from staff.models import NhanVien
from django.shortcuts import redirect
from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import render
def khachhang_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:  # Cho phép admin truy cập
            return view_func(request, *args, **kwargs)
        if not request.user.is_authenticated or not getattr(request.user, 'is_khachhang', False):
            return redirect('login')  # Chuyển hướng nếu không phải khách hàng
        return view_func(request, *args, **kwargs)
    return wrapper


def nhanvien_required(user):
    return user.is_authenticated and user.is_nhanvien()

def phongban_required(allowed_departments=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_staff or request.user.is_superuser:
                return view_func(request, *args, **kwargs)  # Admin always allowed

            try:
                nhanvien = NhanVien.objects.get(user=request.user)
                user_department = nhanvien.MaPhongBan.TenPhongBan.lower()
                if user_department in [d.lower() for d in allowed_departments]:
                    return view_func(request, *args, **kwargs)
            except NhanVien.DoesNotExist:
                pass

            return render(request, 'permission_denied.html')
        return _wrapped_view
    return decorator
