from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('room/', include('room.urls')),
    path('staff/', include('staff.urls')),
    path('api/', include('hello.urls')),
]
