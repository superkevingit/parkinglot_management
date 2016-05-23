from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .forms import CarForm
from .models import Ticket, Car, TicketType, CarType
import json

# 添加车辆视图
def add_car(request):
    if request.method == 'POST':
        car_form = CarForm(request.POST, request.FILES)
        if car_form.is_valid():
            license = car_form.cleaned_data['license']
            car_type = car_form.cleaned_data['cartype']
            car_type = CarType.objects.get(id=car_type)
            ticket_type = car_form.cleaned_data['tickettype']
            ticket_type = TicketType.objects.get(id=ticket_type)
            exist_car = Car.objects.filter(license=license,
                                        cartype=car_type,
                                        tickettype=ticket_type)
            if exist_car.exists():
                messages.add_message(request, messages.ERROR, u"car exist!")
                return HttpResponseRedirect('/add_car')
            else:
                new_car = Car(license=license,
                              cartype=car_type,
                              tickettype=ticket_type)
                new_car.save()
                messages.add_message(request, messages.SUCCESS, u"add car infomation success!")
                return HttpResponseRedirect('/add_car')
    else:
        car_form = CarForm()
    return render(request, 'add_car.html', {'car_form': car_form})
