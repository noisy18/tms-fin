from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from tasks.models import TextTasks, EntryTasks, ExitTasks, KontragentTasks, DeliveryTasks
from tasks.forms import EntryTasksForm, KontragentTasksForm, DeliveryTasksForm
from counterparties.models import CounterParties
from django.utils import timezone

from datetime import datetime, date

# Функция определения сегодняшней даты
def current_date_func(request):
    
    date_str = request.GET.get('date')
    if date_str:
        try:
            chosen_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            chosen_date = today
    else:
        chosen_date = today

    current_date = chosen_date.strftime('%Y-%m-%d')
    return current_date

# Функция определения выбранной даты
def chosen_date_func(request):
    date_str = request.GET.get('date')
    if date_str:
        try:
            chosen_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            chosen_date = today
    else:
        chosen_date = today
    
    return chosen_date

# Кастомный декораторы
def is_cashier(user):
    return user.groups.filter(name='Кассиры').exists()
def is_manager(user):
    return user.groups.filter(name='Менеджеры').exists()
def is_security(user):
    return user.groups.filter(name='Охранники').exists()

# Общие переменные
today = date.today()
now = timezone.now()

def cashier_layout(request):

    context = {
        'username': request.user.username,
    }
    return render(request, 'users/cashier/cashier-layout.html', context)
def manager_layout(request):

    context = {
        'username': request.user.username,
    }
    return render(request, 'users/manager/manager-layout.html', context)
def security_layout(request):

    context = {
        'username': request.user.username,
    }
    return render(request, 'users/security/security-layout.html', context)

# Страницы кассира
@login_required
@user_passes_test(is_cashier)
def cashier_home_page(request):
    context = {
        'username': request.user.username,
        'today': today
    }

    if request.method == 'POST':
        query = request.POST.get('query')
        
        if not query:
            return redirect('cashier_home_page')

        completed_exit_results = ExitTasks.objects.filter(number_auto__icontains=query, is_completed=True, date__gte=today)
        uncompleted_exit_results = ExitTasks.objects.filter(number_auto__icontains=query, is_completed=False, date__gte=today)

        context.update({
            'completed_exit_results': completed_exit_results,
            'uncompleted_exit_results': uncompleted_exit_results,
        })
    return render(request, 'users/cashier/pages/home.html', context)

@login_required
@user_passes_test(is_cashier)
def cashier_exit_page(request):

    exit_tasks = ExitTasks.objects.filter(
        is_completed=False,
        date=chosen_date_func(request)).order_by('-id')
    
    context = {
        'username': request.user.username,
        'exittasks': exit_tasks,
        'current_date': current_date_func(request),

    }
    return render(request, 'users/cashier/pages/exit.html', context)

@login_required
@user_passes_test(is_cashier)
def cashier_edit_exit_task(request, id):
    task = get_object_or_404(ExitTasks, pk=id)
    
    if request.method == 'POST':
        task.is_allowed = 'is_allowed' in request.POST
        
        task.save()
        return redirect('cashier_exit_page')
    
    context = {
        'username': request.user.username,
        'task': task
    }
    return render(request, 'users/cashier/pages/edit-exit-status.html', context)

# Страницы менеджера
@login_required
@user_passes_test(is_manager)
def manager_home_page(request):
    context = {
        'username': request.user.username,
        'today': today
    }

    if request.method == 'POST':
        query = request.POST.get('query')
        
        if not query:
            return redirect('cashier_home_page')

        completed_entry_results = EntryTasks.objects.filter(number_auto__icontains=query, is_completed=True, date__gte=today)
        uncompleted_entry_results = EntryTasks.objects.filter(number_auto__icontains=query, is_completed=False, date__gte=today)

        completed_kontragent = KontragentTasks.objects.filter(number_auto__icontains=query, is_completed=True, date_entry__gte=today)
        uncompleted_kontragent = KontragentTasks.objects.filter(number_auto__icontains=query, is_completed=False, date_entry__gte=today)

        context.update({
            'completed_entry_results': completed_entry_results,
            'uncompleted_entry_results': uncompleted_entry_results,
            'completed_kontragent': completed_kontragent,
            'uncompleted_kontragent': uncompleted_kontragent,
        })
    return render(request, 'users/manager/pages/home.html', context)

@login_required
@user_passes_test(is_manager)
def manager_entry_page(request):

    counterparties = KontragentTasks.objects.filter(
        is_completed=False,
        date_entry__date=chosen_date_func(request)).order_by('-id')

    entry_tasks = EntryTasks.objects.filter(
        is_completed=False,
        date=chosen_date_func(request)).order_by('-id')
    
    context = {
        'username': request.user.username,
        'current_date': current_date_func(request),
        'entrytasks': entry_tasks,
        'counterparties': counterparties,
    }
    return render(request, 'users/manager/pages/entry.html', context)

@login_required
@user_passes_test(is_manager)
def manager_add_entry_task(request):

    if request.method == 'POST':
        form = EntryTasksForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('manager_entry_page')
    else:
        form = EntryTasksForm(user=request.user)

    context = {
        'username': request.user.username,
        'form': form,
    }
    return render(request, 'users/manager/pages/add-entry-task.html', context)

@login_required
@user_passes_test(is_manager)
def manager_edit_entry_task(request, id):
    task = get_object_or_404(EntryTasks, pk=id)

    if request.user != task.author:
        return redirect('manager_entry_page')
    
    if request.method == 'POST':
        task.number_auto = request.POST.get('number_auto')
        task.marka_auto = request.POST.get('marka_auto')
        task.name_organization = request.POST.get('name_organization', '')
        task.date = request.POST.get('date')
        task.time = request.POST.get('time')
        task.description = request.POST.get('description', '')

        task.is_allowed = 'is_allowed' in request.POST
        
        task.save()
        return redirect('manager_entry_page')
    
    context = {
        'username': request.user.username,
        'task': task
    }
    return render(request, 'users/manager/pages/edit-entry-task.html', context)

@login_required
@user_passes_test(is_manager)
def manager_delete_entry_task(request, id):
    task = get_object_or_404(EntryTasks, pk=id)
    
    if request.method == 'POST':
        task.delete()
        return redirect('manager_entry_page')
    
    context = {
        'username': request.user.username,
        'task': task
    }
    return render(request, 'users/manager/pages/modal-win-entry.html', context)

@login_required
@user_passes_test(is_manager)
def manager_add_counterparties(request):
    if request.method == 'POST':
        form = KontragentTasksForm(request.POST, user=request.user)
        if form.is_valid():
            form.author = request.user
            form.save()
            return redirect('manager_entry_page')
    else:
        form = KontragentTasksForm(user=request.user)

    context = {
        'username': request.user.username,
        'form': form,
    }

    return render(request, 'users/manager/pages/add-counterparties.html', context)

@login_required
@user_passes_test(is_manager)
def manager_counterparties_list(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        
        if not query:
            return redirect('counterparties_list')
        
        counterparty = CounterParties.objects.filter(number_auto__icontains=query)
    else:
        counterparty = CounterParties.objects.all()
    context = {
        'username': request.user.username,
        'counterparty': counterparty,
    }

    return render(request, 'users/manager/pages/counterparties-list.html', context)

# Страницы охранника
@login_required
@user_passes_test(is_security)
def security_home_page(request):
    context = {
        'username': request.user.username,
        'today': today
    }

    if request.method == 'POST':
        query = request.POST.get('query')
        
        if not query:
            return redirect('security_home_page')
        
        uncompleted_entry_results = EntryTasks.objects.filter(number_auto__icontains=query, is_completed=False, date=today)

        uncompleted_exit_results = ExitTasks.objects.filter(number_auto__icontains=query, is_completed=False, date=today)

        uncompleted_kontragent = KontragentTasks.objects.filter(number_auto__icontains=query, is_completed=False, date_entry__gte=today)

        uncompleted_delivery = DeliveryTasks.objects.filter(number_auto__icontains=query, is_completed=False, date_entry__gte=today)

        context.update({
            'uncompleted_entry_results': uncompleted_entry_results,
            'uncompleted_exit_results': uncompleted_exit_results,

            'uncompleted_kontragent': uncompleted_kontragent,
            'uncompleted_delivery': uncompleted_delivery,
        })
    return render(request, 'users/security/pages/home.html', context)

@login_required
@user_passes_test(is_security)
def security_entry_page(request):

    entry_tasks = EntryTasks.objects.filter(
        is_completed=False,
        date=chosen_date_func(request),
        date__gte=today).order_by('-id')
    
    context = {
        'username': request.user.username,
        'current_date': current_date_func(request),
        'entrytasks': entry_tasks,
        'today': today,
    }
    return render(request, 'users/security/pages/entry.html', context)

@login_required
@user_passes_test(is_security)
def security_exit_page(request):

    exit_tasks = ExitTasks.objects.filter(
        is_completed=False,
        date=chosen_date_func(request),
        date__gte=today).order_by('-id')
    
    context = {
        'username': request.user.username,
        'current_date': current_date_func(request),
        'exittasks': exit_tasks,
        'today': today,
    }
    return render(request, 'users/security/pages/exit.html', context)

@login_required
@user_passes_test(is_security)
def security_counterparties_page(request):

    counterparties = KontragentTasks.objects.filter(
        is_completed=False,
        date_entry__date=today).order_by('-id')
    
    delivery = DeliveryTasks.objects.filter(
        is_completed=False,
        date_entry__date=today).order_by('-id')

    context = {
        'username': request.user.username,
        'current_date': current_date_func(request),
        'counterparties': counterparties,
        'delivery': delivery
    }
    return render(request, 'users/security/pages/counterparties-delivery.html', context)

@login_required
@user_passes_test(is_security)
def security_tasks_page(request):

    text_tasks = TextTasks.objects.filter(
        is_completed=False,
        date=chosen_date_func(request),
        date__gte=today).order_by('-id')
    
    entry_tasks = EntryTasks.objects.filter(
        is_completed=False,
        date=chosen_date_func(request),
        date__gte=today).order_by('-id')
    
    exit_tasks = ExitTasks.objects.filter(
        is_completed=False,
        date=chosen_date_func(request),
        date__gte=today).order_by('-id')
    
    context = {
        'username': request.user.username,
        'current_date': current_date_func(request),
        'texttasks': text_tasks,
        'entrytasks': entry_tasks,
        'exittasks': exit_tasks,
        'today': today,
    }
    return render(request, 'users/security/pages/tasks-list.html', context)

@login_required
@user_passes_test(is_security)
def security_add_delivery(request):

    if request.method == 'POST':
        form = DeliveryTasksForm(request.POST, user=request.user)
        if form.is_valid():
            form.author = request.user
            form.save()
            return redirect('security_counterparties_page')
    else:
        form = DeliveryTasksForm(user=request.user)

    context = {
        'username': request.user.username,
        'form': form,
    }
    return render(request, 'users/security/pages/add-delivery.html', context)