from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .forms import CarForm
from .models import Ticket, Car
import json


def add_car(request):
    if request.method == 'POST':
        car_form = CarForm(request.POST, request.FILES)
        if car_form.is_valid():
            license = car_form.cleaned_data['license']
            car_type = car_form.cleaned_data['car_type']
            ticket_type = car_form.cleaned_data['ticket_type']
            new_car = Car(license=license,
                          cartype=car_type,
                          tickettype=ticket_type)
            new_car.save()
            messages.add_message(request, messages.SUCCESS, u"add car infomation success!")
            return HttpResponseRedirect('/add_car')
    else:
        car_form = CarForm()
    return render(request, 'add_car.html', {'car_form': car_form})


def ticket_list(request, car_type):
    ticket_list = []
    car_type = request.GET['car_type']
    tickets = Ticket.objects.filter(cartype=car_type)
    for ticket in tickets:
        t = {}
        t['label'] = ticket.tickettype.ticket_type
        t['text'] = ticket.id
        ticket_list.append(t)
    return HttpResponse(json.dumps(ticket_list), content_type='application/json')
