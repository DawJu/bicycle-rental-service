from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime, timedelta
import math
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import User, auth, Group
from .models import *
from .serializers import *

# Create your views here.


def home(request):
    user = request.user
    is_employee = user.groups.filter(name='Employee').exists()
    return render(request, 'main/home.html', {'is_employee': is_employee})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'E-mail zajęty')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Nazwa użytkownika zajęta')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                group = Group.objects.get(name='Basic')
                user.groups.add(group)
                messages.info(request, 'Konto utworzone pomyślnie. Proszę przejść do strony logowania.')
                return redirect('register')
        else:
            messages.info(request, 'Podane hasła nie są identyczne.')
            return redirect('register')
    else:
        return render(request, 'main/register.html', {})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Niepoprawne dane')
            return redirect('log_in')
    else:
        return render(request, 'main/login.html', {})


def profile(request):
    user = request.user
    active_rentals = Rental.objects.filter(
        client__username=user.username, end_time__gte=datetime.now()).order_by('start_time')
    past_rentals = Rental.objects.filter(
        client__username=user.username, end_time__lt=datetime.now()).order_by('start_time')
    return render(request, 'main/profile.html', {
        'active_rentals': active_rentals,
        'past_rentals': past_rentals
    })


def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Nazwa użytkownika jest już zajęta.')
            return redirect('edit_profile')
        if len(username) > 4:
            user.username = username
        elif len(username) > 0:
            messages.info(request, 'Nazwa użytkownika powinna mieć conajmniej 5 znaków.')
            return redirect('edit_profile')
        if len(first_name) > 1:
            user.first_name = first_name
        if len(last_name) > 1:
            user.last_name = last_name
        user.save()
        return redirect('profile')
    else:
        return render(request, 'main/profile_edit.html', {})


def bicycle_list(request):
    user = request.user
    is_employee = user.groups.filter(name='Employee').exists()
    bicycles = Bicycle.objects.all()
    return render(request, 'main/bicycle_list.html', {
        'bicycles': bicycles,
        'is_employee': is_employee
    })


def bicycle_details(request, id):
    user = request.user
    is_employee = user.groups.filter(name='Employee').exists()
    bicycle = Bicycle.objects.get(id=id)
    bicycle_items = BicycleItem.objects.filter(bicycle=bicycle)
    return render(request, 'main/bicycle_details.html', {
        'bicycle': bicycle,
        'bicycle_items': bicycle_items,
        'is_employee': is_employee
    })


def rent_bicycle(request):
    user = request.user
    bicycles = Bicycle.objects.all()
    bicycle_items = BicycleItem.objects.values('info').distinct()
    if request.method == 'POST':
        client = user
        bicycle = request.POST['bicycle']
        bicycle_obj = Bicycle.objects.get(name=bicycle)
        bicycle_item = request.POST['bicycle_item']
        if BicycleItem.objects.filter(info=bicycle_item, bicycle=bicycle_obj).exists():
            bicycle_item_obj = BicycleItem.objects.get(info=bicycle_item, bicycle=bicycle_obj)
        else:
            messages.info(request, 'Nie odnaleziono roweru.')
            return redirect('rent_bicycle')
        start_time = request.POST['start_time']
        start_time_obj = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
        end_time = request.POST['end_time']
        end_time_obj = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')

        if end_time_obj <= start_time_obj:
            messages.info(request, 'Wybrano nieprawidłowe daty rozpoczęcia i zakończenia wypożyczenia.')
            return redirect('rent_bicycle')
        if start_time_obj < datetime.now():
            messages.info(request, 'Wybrano przeszłą datę rozpoczęcia wypożyczenia.')
            return redirect('rent_bicycle')
        if Rental.objects.filter(item=bicycle_item_obj, end_time__gte=start_time_obj).exists():
            messages.info(request, 'Ten rower jest niedostępny w podanym terminie. '
                                   'Proszę wybrać inny rower lub inny termin.')
            return redirect('rent_bicycle')

        hours = (end_time_obj - start_time_obj).total_seconds() / 3600
        num_hours = math.ceil(float(hours))
        total_cost = bicycle_obj.cost * num_hours

        new = Rental.objects.create(start_time=start_time, end_time=end_time, num_hours=num_hours,
                                    total_cost=total_cost, item=bicycle_item_obj, client=client)
        new.save()
        messages.info(request, 'Rower został wypożyczony i czeka gotowy w wypożyczalni w podanym terminie. '
                               'Podgląd wypożyczenia dostępny na profilu użytkownika.')
        return redirect('rent_bicycle')
    else:
        return render(request, 'main/rent_bicycle.html', {
            'bicycles': bicycles,
            'bicycle_items': bicycle_items
        })


def rent_bicycle2(request, id):
    user = request.user
    bicycle = Bicycle.objects.get(id=id)
    bicycle_items = BicycleItem.objects.values('info').distinct()
    if request.method == 'POST':
        client = user
        bicycle_item = request.POST['bicycle_item']
        if BicycleItem.objects.filter(info=bicycle_item, bicycle=bicycle).exists():
            bicycle_item_obj = BicycleItem.objects.get(info=bicycle_item, bicycle=bicycle)
        else:
            messages.info(request, 'Nie odnaleziono roweru.')
            return redirect('rent_bicycle')
        start_time = request.POST['start_time']
        start_time_obj = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
        end_time = request.POST['end_time']
        end_time_obj = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')

        if end_time_obj <= start_time_obj:
            messages.info(request, 'Wybrano nieprawidłowe daty rozpoczęcia i zakończenia wypożyczenia.')
            return redirect('rent_bicycle')
        if start_time_obj < datetime.now():
            messages.info(request, 'Wybrano przeszłą datę rozpoczęcia wypożyczenia.')
            return redirect('rent_bicycle')
        if Rental.objects.filter(item=bicycle_item_obj, end_time__gte=start_time_obj).exists():
            messages.info(request, 'Ten rower jest niedostępny w podanym terminie. '
                                   'Proszę wybrać inny rower lub inny termin.')
            return redirect('rent_bicycle')
        if not BicycleItem.objects.filter(info=bicycle_item, bicycle=bicycle).exists():
            messages.info(request, 'Nie odnaleziono roweru.')
            return redirect('rent_bicycle')

        hours = (end_time_obj - start_time_obj).total_seconds() / 3600
        num_hours = math.ceil(float(hours))
        total_cost = bicycle.cost * num_hours

        new = Rental.objects.create(start_time=start_time, end_time=end_time, num_hours=num_hours,
                                    total_cost=total_cost, item=bicycle_item_obj, client=client)
        new.save()
        messages.info(request, 'Rower został wypożyczony i czeka gotowy w wypożyczalni w podanym terminie. '
                               'Podgląd wypożyczenia dostępny na profilu użytkownika.')
        return redirect('rent_bicycle')
    else:
        return render(request, 'main/rent_bicycle2.html', {
            'bicycle': bicycle,
            'bicycle_items': bicycle_items
        })


def add_report(request):
    user = request.user
    rentals = Rental.objects.filter(client=user, start_time__lte=datetime.now())
    if request.method == 'POST':
        rental_text = request.POST['rental']
        rental_id = int(rental_text.partition('.')[0])
        rental = Rental.objects.get(id=rental_id)
        report = request.POST['report']
        new = Report.objects.create(client=user, text=report, rental=rental, item=rental.item)
        new.save()
        return redirect('/')
    else:
        return render(request, 'main/add_report.html', {'rentals': rentals})


def add_report2(request, id):
    user = request.user
    rental = Rental.objects.get(id=id)
    if request.method == 'POST':
        report = request.POST['report']
        new = Report.objects.create(client=user, text=report, rental=rental, item=rental.item)
        new.save()
        return redirect('/')
    else:
        return render(request, 'main/add_report2.html', {'rental': rental})


def cancel_rental(request, id):
    rental = Rental.objects.get(id=id)
    rental.delete()
    return redirect('profile')


def manage_bicycles(request):
    user = request.user
    is_employee = user.groups.filter(name='Employee').exists()
    bicycles = Bicycle.objects.all()
    return render(request, 'main/emp_bicycles.html', {
        'is_employee': is_employee,
        'bicycles': bicycles
    })


def manage_bicycle_details(request, id):
    user = request.user
    is_employee = user.groups.filter(name='Employee').exists()
    bicycle = Bicycle.objects.get(id=id)
    bicycle_items = BicycleItem.objects.filter(bicycle=bicycle)
    return render(request, 'main/emp_bicycle_details.html', {
        'is_employee': is_employee,
        'bicycle': bicycle,
        'bicycle_items': bicycle_items
    })


def edit_bicycle_details(request, id):
    user = request.user
    is_employee = user.groups.filter(name='Employee').exists()
    bicycle = Bicycle.objects.get(id=id)
    types = Bicycle.Type
    if request.method == 'POST':
        name = request.POST['name']
        type = request.POST['type']
        desc = request.POST['desc']
        cost = request.POST['cost']
        if len(name) > 1:
            bicycle.name = name
        if len(desc) > 5:
            bicycle.desc = desc
        if len(cost) > 0:
            if float(cost) > 0:
                bicycle.cost = float(cost)
        bicycle.type = type
        bicycle.save()
        return redirect('manage_bicycles')
    else:
        return render(request, 'main/emp_bicycle_edit.html', {
            'is_employee': is_employee,
            'bicycle': bicycle,
            'types': types
        })


def delete_bicycle(request, id):
    bicycle = Bicycle.objects.get(id=id)
    bicycle.delete()
    return redirect('manage_bicycles')


def create_bicycle(request):
    user = request.user
    is_employee = user.groups.filter(name='Employee').exists()
    types = Bicycle.Type
    if request.method == 'POST':
        invalid = False
        name = request.POST['name']
        type = request.POST['type']
        desc = request.POST['desc']
        cost = request.POST['cost']
        if len(name) < 2:
            messages.info(request, 'Nazwa musi mieć przynajmniej 2 znaki.')
            invalid = True
        if len(desc) < 5:
            messages.info(request, 'Opis musi mieć przynajmniej 5 znaków.')
            invalid = True
        if len(cost) < 1:
            messages.info(request, 'Nie podano ceny.')
            invalid = True
        elif float(cost) <= 0:
            messages.info(request, 'Cena musi być większa od 0.')
            invalid = True
        if invalid:
            return redirect('create_bicycle')
        bicycle = Bicycle.objects.create(name=name, type=type, desc=desc, cost=float(cost))
        bicycle.save()
        return redirect('manage_bicycles')
    else:
        return render(request, 'main/emp_bicycle_create.html', {
            'is_employee': is_employee,
            'types': types
        })


def create_bicycle2(request):
    user = request.user
    is_employee = user.groups.filter(name='Employee').exists()
    bicycles = Bicycle.objects.all()
    if request.method == 'POST':
        bicycle = request.POST['bicycle']
        bicycle_obj = Bicycle.objects.get(name=bicycle)
        info = request.POST['info']
        if len(info) < 2:
            messages.info(request, 'Informacja musi mieć przynajmniej 2 znaki.')
            return redirect('create_bicycle2')
        new = BicycleItem.objects.create(bicycle=bicycle_obj, info=info)
        new.save()
        return redirect('manage_bicycles')
    else:
        return render(request, 'main/emp_bicycle_create2.html', {
            'is_employee': is_employee,
            'bicycles': bicycles
        })


def delete_bicycle2(request, id):
    bicycle_item = BicycleItem.objects.get(id=id)
    bicycle_item.delete()
    return redirect('manage_bicycles')


def manage_rentals(request):
    user = request.user
    is_employee = user.groups.filter(name='Employee').exists()
    active_rentals = Rental.objects.filter(end_time__gte=datetime.now()).order_by('start_time')
    past_rentals = Rental.objects.filter(end_time__lt=datetime.now()).order_by('start_time')
    return render(request, 'main/emp_rentals.html', {
        'is_employee': is_employee,
        'active_rentals': active_rentals,
        'past_rentals': past_rentals
    })


def rental_details(request, id):
    user = request.user
    is_employee = user.groups.filter(name='Employee').exists()
    rental = Rental.objects.get(id=id)
    return render(request, 'main/emp_rental_details.html', {
        'is_employee': is_employee,
        'rental': rental
    })


def manage_reports(request):
    user = request.user
    is_employee = user.groups.filter(name='Employee').exists()
    reports = Report.objects.all()
    return render(request, 'main/emp_reports.html', {
        'is_employee': is_employee,
        'reports': reports
    })


def report_details(request, id):
    user = request.user
    is_employee = user.groups.filter(name='Employee').exists()
    report = Report.objects.get(id=id)
    return render(request, 'main/emp_report_details.html', {
        'is_employee': is_employee,
        'report': report
    })
