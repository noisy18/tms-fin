from django.shortcuts import render, get_object_or_404, redirect
from counterparties.models import CounterParties
from tasks.models import KontragentTasks

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Администраторы').exists()

def create_counterparty_pass(request, counterparty_id):
    if request.method == "POST":
        counterparty = get_object_or_404(CounterParties, id=counterparty_id)

        KontragentTasks.objects.create(
            number_auto = counterparty.number_auto,
            author = request.user,
            description = f'Марка авто: {counterparty.marka_auto}'
        )

        if is_admin(request.user):
            return redirect('counterparties_page')
        elif request.user.groups.filter(name='Менеджеры').exists():
            return redirect('manager_entry_page')
    if is_admin(request.user):
        return redirect('counterparties_list')
    elif request.user.groups.filter(name='Менеджеры').exists():
        return redirect('manager_counterparties_list')
    

def edit_counterparty(request, counterparty_id):
    counterparty = get_object_or_404(CounterParties, id=counterparty_id)

    if request.method == 'POST':
        counterparty.name = request.POST.get('name')
        counterparty.surname = request.POST.get('surname')
        counterparty.last_name = request.POST.get('last_name')
        counterparty.marka_auto = request.POST.get('marka_auto')
        counterparty.number_auto = request.POST.get('number_auto')
        counterparty.vin_number = request.POST.get('vin_number')
        counterparty.save()
        return redirect('counterparties_list')
    
    context = {
        'username': request.user.username,
        'counterparty': counterparty,
    }

    return render(request, 'tms_admin/additional-pages/edit-forms/counterparty-form.html', context)