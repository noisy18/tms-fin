from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login/')
def login_check(request):
    if request.user.is_superuser or request.user.groups.filter(name='Администраторы').exists():
        return redirect('admin_home_page')
    elif request.user.groups.filter(name='Кассиры').exists():
        return redirect('cashier_home_page')
    elif request.user.groups.filter(name='Охранники').exists():
        return redirect('security_home_page')
    elif request.user.groups.filter(name='Менеджеры').exists():
        return redirect('manager_home_page')
    else:
        return redirect('login')
