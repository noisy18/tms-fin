from django.shortcuts import render, get_object_or_404, redirect
from counterparties.models import CounterParties, CounterpartyCars
from tasks.models import KontragentTasks

from counterparties.forms import CounterPartyCarsForm

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Администраторы').exists()

def create_car_pass(request, car_id):
    if request.method == "POST":
        counterparty = get_object_or_404(CounterpartyCars, id=car_id)

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
        counterparty.inn = request.POST.get('inn')
        counterparty.kpp = request.POST.get('kpp')
        counterparty.okpo = request.POST.get('okpo')
        counterparty.ogrn = request.POST.get('ogrn')
        counterparty.save()
        return redirect('counterparties_list')
    
    context = {
        'username': request.user.username,
        'counterparty': counterparty,
    }

    return render(request, 'tms_admin/additional-pages/edit-forms/counterparty-form.html', context)

def cars_info(request, counterparty_id):
    counterparty = get_object_or_404(CounterParties, id=counterparty_id)
    cars = CounterpartyCars.objects.filter(counterparty=counterparty)
    context = {
        'username': request.user.username,
        'counterparty': counterparty,
        'cars': cars,
    }

    return render(request, 'tms_admin/additional-pages/cars-info/cars-info.html', context)

def add_car(request, counterparty_id):
    counterparty = get_object_or_404(CounterParties, id=counterparty_id)

    if request.method == 'POST':
        form = CounterPartyCarsForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.counterparty_id = counterparty.id 
            instance.save()
            return redirect('cars_info', counterparty_id=counterparty.id)
    else:
        form = CounterPartyCarsForm()


    context = {
        'username': request.user.username,
        'counterparty': counterparty,
        'form': form,
    }
    return render(request, 'tms_admin/additional-pages/cars-info/add-cars.html', context)

def edit_car(request, car_id, counterparty_id):
    counterparty = get_object_or_404(CounterParties, id=counterparty_id)
    car = get_object_or_404(CounterpartyCars, id=car_id)
    
    if request.method == 'POST':
        car.full_name = request.POST.get('full_name')
        car.number_auto = request.POST.get('number_auto')
        car.vin_number = request.POST.get('vin_number')
        car.marka_auto = request.POST.get('marka_auto')
        car.model_auto = request.POST.get('model_auto')
        car.release_date = request.POST.get('release_date')
        car.save()

        return redirect('cars_info', counterparty_id=counterparty.id)

    context = {
        'username': request.user.username,
        'counterparty': counterparty,
        'car': car,
    }
    return render(request, 'tms_admin/additional-pages/cars-info/edit-car.html', context)