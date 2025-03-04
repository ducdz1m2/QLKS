from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import DichVu
from .forms import DichVuForm

def service_list(request):
    services = DichVu.objects.all()
    return render(request, 'service/service_list.html', {'services': services})

def add_service(request):
    if request.method == 'POST':
        form = DichVuForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thêm dịch vụ thành công!")
            return redirect('service_list')
    else:
        form = DichVuForm()
    return render(request, 'service/add_service.html', {'form': form})

def edit_service(request, pk):
    service = get_object_or_404(DichVu, pk=pk)
    if request.method == 'POST':
        form = DichVuForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật dịch vụ thành công!")
            return redirect('service_list')
    else:
        form = DichVuForm(instance=service)
    return render(request, 'service/edit_service.html', {'form': form})

def delete_service(request, pk):
    service = get_object_or_404(DichVu, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, "Xóa dịch vụ thành công!")
        return redirect('service_list')
    return render(request, 'service/delete_service.html', {'service': service})