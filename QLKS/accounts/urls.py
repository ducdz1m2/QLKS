from django.urls import path
from .views import logout_view  # Import chính xác view logout

urlpatterns = [
    path('logout/', logout_view, name='logout'),  # Định tuyến logout
]
