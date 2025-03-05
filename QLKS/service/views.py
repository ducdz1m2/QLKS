from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from .forms import DichVuForm, SuDungDichVuForm

#Dich vu
def service_list(request):
    services = get_all_services()
    return render(request, 'service/service_list.html', {'services': services})

def get_service(pk):
    with connection.cursor() as cursor:
        cursor.callproc('GetService', [pk])
        columns = [col[0] for col in cursor.description]
        result = cursor.fetchone()
        return dict(zip(columns, result)) if result else None

def get_all_services():
    with connection.cursor() as cursor:
        cursor.callproc('GetAllService')
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def add_service(request):
    if request.method == 'POST':
        form = DichVuForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.callproc('AddService', [form.cleaned_data['TenDichVu'], form.cleaned_data['GiaDichVu']])
            messages.success(request, "Thêm dịch vụ thành công!")
            return redirect('service_list')
    else:
        form = DichVuForm()
    return render(request, 'service/add_service.html', {'form': form})

def edit_service(request, pk):
    service = get_service(pk)
    if not service:
        return redirect('service_list')
    if request.method == 'POST':
        form = DichVuForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.callproc('UpdateService', [pk, form.cleaned_data['TenDichVu'], form.cleaned_data['GiaDichVu']])
            messages.success(request, "Cập nhật dịch vụ thành công!")
            return redirect('service_list')
    else:
        form = DichVuForm(initial={
            'TenDichVu': service.get('TenDichVu'),
            'GiaDichVu': service.get('GiaDichVu')
        })
    return render(request, 'service/edit_service.html', {'form': form})

def delete_service(request, pk):
    service = get_service(pk)
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.callproc('DeleteService', [pk])
        messages.success(request, "Xóa dịch vụ thành công!")
        return redirect('service_list')
    return render(request, 'service/delete_service.html', {'service': service})

#Su dung dich vu
def usage_list(request):
    usages = get_all_usages()
    return render(request, 'usage/usage_list.html', {'usages': usages})

def get_usage(pk):
    with connection.cursor() as cursor:
        cursor.callproc('GetUsage', [pk])
        columns = [col[0] for col in cursor.description]
        result = cursor.fetchone()
        return dict(zip(columns, result)) if result else None

def get_all_usages():
    with connection.cursor() as cursor:
        cursor.callproc('GetAllUsage')
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def add_usage(request):
    from .forms import SuDungDichVuForm
    if request.method == 'POST':
        form = SuDungDichVuForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.callproc(
                    'AddUsage',
                    [
                        form.cleaned_data['MaThue'],
                        form.cleaned_data['MaDichVu'],
                        form.cleaned_data['SoLuong'],
                        form.cleaned_data['NgaySuDung']
                    ]
                )
            messages.success(request, "Thêm sử dụng dịch vụ thành công!")
            return redirect('usage_list')
    else:
        form = SuDungDichVuForm()
    return render(request, 'usage/add_usage.html', {'form': form})

def edit_usage(request, pk):
    from .forms import SuDungDichVuForm
    usage = get_usage(pk)
    if not usage:
        return redirect('usage_list')
    if request.method == 'POST':
        form = SuDungDichVuForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.callproc(
                    'UpdateUsage',
                    [
                        pk,
                        form.cleaned_data['MaThue'],
                        form.cleaned_data['MaDichVu'],
                        form.cleaned_data['SoLuong'],
                        form.cleaned_data['NgaySuDung']
                    ]
                )
            messages.success(request, "Cập nhật sử dụng dịch vụ thành công!")
            return redirect('usage_list')
    else:
        form = SuDungDichVuForm(initial={
            'MaThue': usage.get('MaThue'),
            'MaDichVu': usage.get('MaDichVu'),
            'SoLuong': usage.get('SoLuong'),
            'NgaySuDung': usage.get('NgaySuDung')
        })
    return render(request, 'usage/edit_usage.html', {'form': form})

def delete_usage(request, pk):
    usage = get_usage(pk)
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.callproc('DeleteSudungdichvu', [pk])
        messages.success(request, "Xóa sử dụng dịch vụ thành công!")
        return redirect('usage_list')
    return render(request, 'usage/delete_usage.html', {'usage': usage})