from django.urls import path
from .views import * # Import chính xác view logout

urlpatterns = [
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),  # Định tuyến logout
    path('redirect/', redirect_user_home, name='redirect_home'),
]
