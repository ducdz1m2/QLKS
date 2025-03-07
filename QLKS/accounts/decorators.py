from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import redirect
from functools import wraps

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
