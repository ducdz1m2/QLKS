from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Tắt CSRF để logout dễ dàng hơn (có thể bỏ nếu không cần)
def logout_view(request):
    if request.method in ['POST', 'GET']:  # Cho phép cả GET và POST
        logout(request)
        return redirect('/accounts/login/')
    return redirect('/')  # Nếu request không hợp lệ, quay về trang chủ
