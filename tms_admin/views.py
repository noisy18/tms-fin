from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.utils import timezone

from tasks.models import (
    TextTasks, 
    EntryTasks,
    ExitTasks,
    KontragentTasks,
    DeliveryTasks)
from tasks.forms import (
    TextTasksForm,
    EntryTasksForm,
    ExitTasksForm,
    CombinedProfileChangeForm,
    CustomUserCreationForm,
    CustomUserChangeForm,
    KontragentTasksForm,
    DeliveryTasksForm)

from counterparties.models import CounterParties

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

# Кастомный декоратор
def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Администраторы').exists()

# Общие переменные
today = date.today()
now = timezone.now()


# Представления основных страниц

def admin_layout(request):
    context = {
        'username': request.user.username,
    }
    return render(request, 'tms_admin/admin-layout.html', context)

@login_required
@user_passes_test(is_admin)
def admin_home_page(request):
    context = {
        'username': request.user.username,
        'today': today
    }

    if request.method == 'POST':
        query = request.POST.get('query')
        
        if not query:
            return redirect('admin_home_page')
        
        completed_entry_results = EntryTasks.objects.filter(number_auto__icontains=query, is_completed=True)
        uncompleted_entry_results = EntryTasks.objects.filter(number_auto__icontains=query, is_completed=False)

        completed_exit_results = ExitTasks.objects.filter(number_auto__icontains=query, is_completed=True)
        uncompleted_exit_results = ExitTasks.objects.filter(number_auto__icontains=query, is_completed=False)

        completed_kontragent = KontragentTasks.objects.filter(number_auto__icontains=query, is_completed=True)
        uncompleted_kontragent = KontragentTasks.objects.filter(number_auto__icontains=query, is_completed=False)

        completed_delivery = DeliveryTasks.objects.filter(number_auto__icontains=query, is_completed=True)
        uncompleted_delivery = DeliveryTasks.objects.filter(number_auto__icontains=query, is_completed=False)

        context.update({
            'completed_entry_results': completed_entry_results,
            'uncompleted_entry_results': uncompleted_entry_results,
            'completed_exit_results': completed_exit_results,
            'uncompleted_exit_results': uncompleted_exit_results,

            'completed_kontragent': completed_kontragent,
            'uncompleted_kontragent': uncompleted_kontragent,
            'completed_delivery': completed_delivery,
            'uncompleted_delivery': uncompleted_delivery,
            'now': now
        })

    return render(request, 'tms_admin/pages/home.html', context)

@login_required
@user_passes_test(is_admin)
def entry_page(request):

    entry_tasks = EntryTasks.objects.filter(
        is_completed=False,
        date=chosen_date_func(request)).order_by('-id')
    
    context = {
        'username': request.user.username,
        'current_date': current_date_func(request),
        'entrytasks': entry_tasks,
    }
    return render(request, 'tms_admin/pages/entry.html', context)

@login_required
@user_passes_test(is_admin)
def exit_page(request):

    exit_tasks = ExitTasks.objects.filter(
        is_completed=False,
        date=chosen_date_func(request)).order_by('-id')
    
    context = {
        'username': request.user.username,
        'current_date': current_date_func(request),
        'exittasks': exit_tasks,
    }
    return render(request, 'tms_admin/pages/exit.html', context)

@login_required
@user_passes_test(is_admin)
def counterparties_page(request):
    counterparties = KontragentTasks.objects.filter(
        is_completed=False,
        date_entry__date=chosen_date_func(request)).order_by('-id')
    
    delivery = DeliveryTasks.objects.filter(
        is_completed=False,
        date_entry__date=chosen_date_func(request)).order_by('-id')

    context = {
        'username': request.user.username,
        'current_date': current_date_func(request),
        'counterparties': counterparties,
        'delivery': delivery
    }
    return render(request, 'tms_admin/pages/counterparties-delivery.html', context)

@login_required
@user_passes_test(is_admin)
def counterparties_list(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        
        if not query:
            return redirect('counterparties_list')
        
        counterparty = CounterParties.objects.filter(name__icontains=query)
    else:
        counterparty = CounterParties.objects.all()

    context = {
        'counterparty': counterparty,
        'username': request.user.username,
        'current_date': current_date_func(request),
    }
    return render(request, 'tms_admin/pages/counterperties-list.html', context)

@login_required
@user_passes_test(is_admin)
def tasks_page(request):

    text_tasks = TextTasks.objects.filter(
        is_completed=False,
        date=chosen_date_func(request)).order_by('-id')
    
    entry_tasks = EntryTasks.objects.filter(
        is_completed=False,
        date=chosen_date_func(request)).order_by('-id')
    
    exit_tasks = ExitTasks.objects.filter(
        is_completed=False,
        date=chosen_date_func(request)).order_by('-id')
    
    context = {
        'username': request.user.username,
        'current_date': current_date_func(request),
        'texttasks': text_tasks,
        'entrytasks': entry_tasks,
        'exittasks': exit_tasks,
    }
    return render(request, 'tms_admin/pages/tasks-list.html', context)

@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    users_in_group = User.objects.filter(
        Q(groups__name='Менеджеры') | Q(groups__name='Кассиры') | Q(groups__name='Охранники')
    )

    if request.method == 'POST':
        profile_form = CombinedProfileChangeForm(user=request.user, data=request.POST)
        user_creation_form = CustomUserCreationForm(data=request.POST)
        
        if 'edit_profile_submit' in request.POST:
            if profile_form.is_valid():
                profile_form.save()
                update_session_auth_hash(request, profile_form.user)
                return redirect('admin_home_page')
        
        elif 'add_user_submit' in request.POST:
            if user_creation_form.is_valid():
                username = user_creation_form.cleaned_data['username']
                password = user_creation_form.cleaned_data['password1']

                new_user = User.objects.create_user(username=username, password=password)

                group_name = None
                if request.POST['selected_option'] == 'option1':
                    group_name = 'Менеджеры'
                elif request.POST['selected_option'] == 'option2':
                    group_name = 'Кассиры'
                elif request.POST['selected_option'] == 'option3':
                    group_name = 'Охранники'

                if group_name is not None:
                    group = Group.objects.get(name=group_name)
                    new_user.groups.add(group)
                    new_user.save()

                return redirect('admin_home_page')
    
    else:
        profile_form = CombinedProfileChangeForm(user=request.user)
        user_creation_form = CustomUserCreationForm()

    context = {
        'username': request.user.username,
        'current_date': current_date_func(request),
        'profile_form': profile_form,
        'user_creation_form': user_creation_form,
        'users_in_group': users_in_group
    }
    return render(request, 'tms_admin/pages/admin-panel.html', context)

@login_required
@user_passes_test(is_admin)
def tasks_archive(request):
    filter_type = request.GET.get('filterType')
    filter_value = request.GET.get('filterValue')
    filter_status = request.GET.get('completedStatusSelect')

    completed_text_tasks = None
    completed_entry_tasks = None
    completed_exit_tasks = None

    uncompleted_text_tasks = None
    uncompleted_entry_tasks = None
    uncompleted_exit_tasks = None
    
    # Фильтруем задачи в зависимости от типа фильтра
    if filter_type == 'date':
        try:
            search_date = datetime.strptime(filter_value, '%Y-%m-%d').date()
        except ValueError:
            search_date = today

        completed_text_tasks = TextTasks.objects.filter(date=search_date, is_completed=True, date__lt=today).order_by('-id')
        uncompleted_text_tasks = TextTasks.objects.filter(date=search_date, is_completed=False, date__lt=today).order_by('-id')

        completed_entry_tasks = EntryTasks.objects.filter(date=search_date, is_completed=True, date__lt=today).order_by('-id')
        uncompleted_entry_tasks = EntryTasks.objects.filter(date=search_date, is_completed=False, date__lt=today).order_by('-id')

        completed_exit_tasks = ExitTasks.objects.filter(date=search_date, is_completed=True, date__lt=today).order_by('-id')
        uncompleted_exit_tasks = ExitTasks.objects.filter(date=search_date, is_completed=False, date__lt=today).order_by('-id')

    elif filter_type == 'carNumber' and filter_value:
        completed_entry_tasks = EntryTasks.objects.filter(number_auto=filter_value, is_completed=True, date__lt=today).order_by('-id')
        uncompleted_entry_tasks = EntryTasks.objects.filter(number_auto=filter_value, is_completed=False, date__lt=today).order_by('-id')

        completed_exit_tasks = ExitTasks.objects.filter(number_auto=filter_value, is_completed=True, date__lt=today).order_by('-id')
        uncompleted_exit_tasks = ExitTasks.objects.filter(number_auto=filter_value, is_completed=False, date__lt=today).order_by('-id')

    elif filter_type == 'completedStatus':
        if filter_status == 'true':
            completed_text_tasks = TextTasks.objects.filter(is_completed=True, date__lt=today).order_by('-id')
            completed_entry_tasks = EntryTasks.objects.filter(is_completed=True, date__lt=today).order_by('-id')
            completed_exit_tasks = ExitTasks.objects.filter(is_completed=True, date__lt=today).order_by('-id')

        elif filter_status == 'false':
            uncompleted_text_tasks = TextTasks.objects.filter(is_completed=False, date__lt=today).order_by('-id')
            uncompleted_entry_tasks = EntryTasks.objects.filter(is_completed=False, date__lt=today).order_by('-id')
            uncompleted_exit_tasks = ExitTasks.objects.filter(is_completed=False, date__lt=today).order_by('-id')
    else:
        completed_text_tasks = TextTasks.objects.filter(date__lt=today, is_completed=True).order_by('-id')
        completed_entry_tasks = EntryTasks.objects.filter(date__lt=today, is_completed=True).order_by('-id')
        completed_exit_tasks = ExitTasks.objects.filter(date__lt=today, is_completed=True).order_by('-id')

        uncompleted_text_tasks = TextTasks.objects.filter(date__lt=today, is_completed=False).order_by('-id')
        uncompleted_entry_tasks = EntryTasks.objects.filter(date__lt=today, is_completed=False).order_by('-id')
        uncompleted_exit_tasks = ExitTasks.objects.filter(date__lt=today, is_completed=False).order_by('-id')

    context = {
        'username': request.user.username,
        'current_date': chosen_date_func(request),

        'completed_text_results': completed_text_tasks,
        'uncompleted_text_results': uncompleted_text_tasks,
        'completed_entry_results': completed_entry_tasks,
        'uncompleted_entry_results': uncompleted_entry_tasks,
        'completed_exit_results': completed_exit_tasks,
        'uncompleted_exit_results': uncompleted_exit_tasks
    }
    
    return render(request, 'tms_admin/pages/tasks-archive.html', context)

# Представления дополнительных страниц

@login_required
@user_passes_test(is_admin)
def completed_tasks(request):
    completed_entry_tasks = EntryTasks.objects.filter(is_completed=True, completed_at__date=today)
    completed_exit_tasks = ExitTasks.objects.filter(is_completed=True, completed_at__date=today)
    completed_text_tasks = TextTasks.objects.filter(is_completed=True, completed_at__date=today)

    context = {
        'username': request.user.username,
        'completed_entry_tasks': completed_entry_tasks,
        'completed_exit_tasks': completed_exit_tasks,
        'completed_text_tasks': completed_text_tasks,
    }
    return render(request, 'tms_admin/additional-pages/completed-tasks/completed-tasks.html', context)

@login_required
@user_passes_test(is_admin)
def counterparties_archive(request):
    filter_type = request.GET.get('filterType')
    filter_value = request.GET.get('filterValue')
    filter_status = request.GET.get('completedStatusSelect')

    completed_counterparties = None
    uncompleted_counterparties = None
    completed_delivery = None
    uncompleted_delivery = None

    if filter_type == 'carNumber' and filter_value:
        completed_counterparties = KontragentTasks.objects.filter(number_auto=filter_value, is_completed=True).order_by('-id')
        completed_delivery = DeliveryTasks.objects.filter(number_auto=filter_value, is_completed=True).order_by('-id')

        uncompleted_counterparties = KontragentTasks.objects.filter(number_auto=filter_value, is_completed=False, date_entry__date__lt=today).order_by('-id')
        uncompleted_delivery = DeliveryTasks.objects.filter(number_auto=filter_value, is_completed=False, date_entry__date__lt=today).order_by('-id')

    elif filter_type == 'completedStatus':
        if filter_status == 'true':
            completed_counterparties = KontragentTasks.objects.filter(is_completed=True).order_by('-id')
            completed_delivery = DeliveryTasks.objects.filter(is_completed=True).order_by('-id')

        elif filter_status == 'false':
            uncompleted_counterparties = KontragentTasks.objects.filter(is_completed=False, date_entry__date__lt=today).order_by('-id')
            uncompleted_delivery = DeliveryTasks.objects.filter(is_completed=False, date_entry__date__lt=today).order_by('-id')

    else:
        completed_counterparties = KontragentTasks.objects.filter(is_completed=True).order_by('-id')
        completed_delivery = DeliveryTasks.objects.filter(is_completed=True).order_by('-id')

        uncompleted_counterparties = KontragentTasks.objects.filter(is_completed=False, date_entry__date__lt=today).order_by('-id')
        uncompleted_delivery = DeliveryTasks.objects.filter(is_completed=False, date_entry__date__lt=today).order_by('-id')

    context = {
        'username': request.user.username,
        'completed_counterparties': completed_counterparties,
        'completed_delivery': completed_delivery,
        'uncompleted_counterparties': uncompleted_counterparties,
        'uncompleted_delivery': uncompleted_delivery
    }
    return render(request, 'tms_admin/additional-pages/counterparties-archive/counterparties-archive.html', context)

@login_required
@user_passes_test(is_admin)
def edit_user_form(request, id):
    user_to_edit = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            form.save()
            return redirect('admin_home_page')
    else:
        form = CustomUserChangeForm(instance=user_to_edit)

    context = {
        'form': form,
        'username': request.user.username,
        'user_to_edit': user_to_edit
    }

    return render(request, 'tms_admin/additional-pages/edit-user/edit-user-form.html', context)

@login_required
@user_passes_test(is_admin)
def delete_user(request, id):
    user_to_delete = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        user_to_delete.delete()
        return redirect('admin_home_page')
    
    context = {
        'username': request.user.username,
        'user_to_delete': user_to_delete,
    }
    return render(request, 'tms_admin/additional-pages/modal-wins/modal-win-user.html', context)

# Формы добавления

@login_required
@user_passes_test(is_admin)
def add_text_task(request):

    if request.method == 'POST':
        form = TextTasksForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('tasks_page')
    else:
        form = TextTasksForm(user=request.user)
    
    context = {
        'username': request.user.username,
        'form': form,
    }
    return render(request, 'tms_admin/additional-pages/add-forms/text-form.html', context)

@login_required
@user_passes_test(is_admin)
def add_entry_task(request):

    if request.method == 'POST':
        form = EntryTasksForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('tasks_page')
    else:
        form = EntryTasksForm(user=request.user)

    context = {
        'username': request.user.username,
        'form': form,
    }
    return render(request, 'tms_admin/additional-pages/add-forms/entry-form.html', context)

@login_required
@user_passes_test(is_admin)
def add_exit_task(request):
    if request.method == 'POST':
        form = ExitTasksForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('tasks_page')
    else:
        form = ExitTasksForm(user=request.user)

    context = {
        'username': request.user.username,
        'form': form,
    }
    return render(request, 'tms_admin/additional-pages/add-forms/exit-form.html', context)

@login_required
@user_passes_test(is_admin)
def add_delivery(request):
    if request.method == 'POST':
        form = DeliveryTasksForm(request.POST, user=request.user)
        if form.is_valid():
            form.author = request.user
            form.save()
            return redirect('counterparties_page')
    else:
        form = DeliveryTasksForm(user=request.user)

    context = {
        'username': request.user.username,
        'form': form,
    }
    return render(request, 'tms_admin/additional-pages/add-forms/delivery-form.html', context)

# Формы редактирования

@login_required
@user_passes_test(is_admin)
def edit_text_task(request, id):
    task = get_object_or_404(TextTasks, pk=id)

    if request.user != task.author:
        return redirect('tasks_page')
    
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.full_text = request.POST.get('full_text', '')
        task.save()
        return redirect('tasks_page')
    
    context = {
        'username': request.user.username,
        'task': task
    }
    return render(request, 'tms_admin/additional-pages/edit-forms/text-form.html', context)

@login_required
@user_passes_test(is_admin)
def delete_text_task(request, id):
    task = get_object_or_404(TextTasks, pk=id)
    
    if request.method == 'POST':
        task.delete()
        return redirect('tasks_page')
    
    context = {
        'username': request.user.username,
        'task': task
    }
    return render(request, 'tms_admin/additional-pages/modal-wins/modal-win-text.html', context)

@login_required
@user_passes_test(is_admin)
def edit_entry_task(request, id):
    task = get_object_or_404(EntryTasks, pk=id)

    if request.user != task.author:
        return redirect('tasks_page')
    
    if request.method == 'POST':
        task.number_auto = request.POST.get('number_auto')
        task.marka_auto = request.POST.get('marka_auto')
        task.name_organization = request.POST.get('name_organization', '')
        task.date = request.POST.get('date')
        task.time = request.POST.get('time')
        task.description = request.POST.get('description', '')

        task.is_allowed = 'is_allowed' in request.POST
        
        task.save()
        return redirect('tasks_page')
    
    context = {
        'username': request.user.username,
        'task': task
    }
    return render(request, 'tms_admin/additional-pages/edit-forms/entry-form.html', context)

@login_required
@user_passes_test(is_admin)
def delete_entry_task(request, id):
    task = get_object_or_404(EntryTasks, pk=id)
    
    if request.method == 'POST':
        task.delete()
        return redirect('tasks_page')
    
    context = {
        'username': request.user.username,
        'task': task
    }
    return render(request, 'tms_admin/additional-pages/modal-wins/modal-win-entry.html', context)

@login_required
@user_passes_test(is_admin)
def edit_exit_task(request, id):
    task = get_object_or_404(ExitTasks, pk=id)

    if request.user != task.author:
        return redirect('tasks_page')
    
    if request.method == 'POST':
        task.number_auto = request.POST.get('number_auto')
        task.marka_auto = request.POST.get('marka_auto')
        task.name_organization = request.POST.get('name_organization', '')
        task.date = request.POST.get('date')
        task.time = request.POST.get('time')
        task.description = request.POST.get('description', '')

        task.is_allowed = 'is_allowed' in request.POST
        
        task.save()
        return redirect('tasks_page')
    
    context = {
        'username': request.user.username,
        'task': task
    }
    return render(request, 'tms_admin/additional-pages/edit-forms/exit-form.html', context)

@login_required
@user_passes_test(is_admin)
def delete_exit_task(request, id):
    task = get_object_or_404(ExitTasks, pk=id)
    
    if request.method == 'POST':
        task.delete()
        return redirect('tasks_page')
    
    context = {
        'username': request.user.username,
        'task': task
    }
    return render(request, 'tms_admin/additional-pages/modal-wins/modal-win-exit.html', context)

# Изменение статуса

def mark_text_task_complete(request, id):
    if request.method == 'POST':
        task = get_object_or_404(TextTasks, id=id)
        task.is_completed = True
        task.completed_at = datetime.now()
        task.completed_by = request.user
        task.save()

        if is_admin(request.user):
            return redirect('tasks_page')
        elif request.user.groups.filter(name='Охранники').exists():
            return redirect('security_tasks_page')

def mark_entry_task_complete(request, id):
    if request.method == 'POST':
        task = get_object_or_404(EntryTasks, id=id)
        task.is_completed = True
        task.completed_at = datetime.now()
        task.completed_by = request.user
        task.save()

        if is_admin(request.user):
            return redirect('tasks_page')
        elif request.user.groups.filter(name='Охранники').exists():
            return redirect('security_tasks_page')

def mark_exit_task_complete(request, id):
    if request.method == 'POST':
        task = get_object_or_404(ExitTasks, id=id)
        task.is_completed = True
        task.completed_at = datetime.now()
        task.completed_by = request.user
        task.save()

        if is_admin(request.user):
            return redirect('tasks_page')
        elif request.user.groups.filter(name='Охранники').exists():
            return redirect('security_tasks_page')
        
def mark_counterparties_complete(request, id):
    if request.method == 'POST':
        task = get_object_or_404(KontragentTasks, id=id)
        task.is_completed = True
        task.date_exit = datetime.now()
        task.completed_by = request.user
        task.save()

        # Проверяем группу пользователя
        if is_admin(request.user):
            return redirect('counterparties_page')
        elif request.user.groups.filter(name='Охранники').exists():
            return redirect('security_counterparties_page')
        
def mark_delivery_complete(request, id):
    if request.method == 'POST':
        task = get_object_or_404(DeliveryTasks, id=id)
        task.is_completed = True
        task.date_exit = datetime.now()
        task.completed_by = request.user
        task.save()

        # Проверяем группу пользователя
        if is_admin(request.user):
            return redirect('counterparties_page')
        elif request.user.groups.filter(name='Охранники').exists():
            return redirect('security_counterparties_page')
