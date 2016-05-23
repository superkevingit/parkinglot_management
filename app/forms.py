#!/usr/bin/env python
# encoding: utf-8
from django import forms
from .models import CarType, TicketType


car_types = CarType.objects.all()
car_type_choice = []
for car_type in car_types:
    car_type_choice.append([car_type.id, car_type.car_type])

ticket_types = TicketType.objects.all()
ticket_type_choice = []
for ticket_type in ticket_types:
    ticket_type_choice.append([ticket_type.id, ticket_type.ticket_type])


class CarForm(forms.Form):
    license = forms.CharField(max_length=50, label=u'车牌')
    cartype = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'select'}),
        choices=car_type_choice,
        label=u'选择车辆类型')
    tickettype = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'select'}),
        choices=ticket_type_choice,
        label=u'选择购票类型')
