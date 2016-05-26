#!/usr/bin/env python
# encoding: utf-8
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import CarType, Car, TicketType


car_types = CarType.objects.all()
car_type_choice = []
for car_type in car_types:
    car_type_choice.append([car_type.id, car_type.car_type])

ticket_types = TicketType.objects.all()
ticket_type_choice = []
for ticket_type in ticket_types:
    ticket_type_choice.append([ticket_type.id, ticket_type.ticket_type])


class UserForm(forms.ModelForm):
    username= forms.CharField(widget=forms.TextInput(
        attrs={'type': "text", 'id': "inputText", 'class': 'form-control', 'placeholder': u'用户名', 'required autofocus': ''}), label=u'用户名')
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'type': "email", 'id': "inputEmail", 'class': 'form-control', 'placeholder': u'邮箱', 'required': ''}), label=u'邮箱')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'type': "password", 'id': "inputPassword", 'class': 'form-control', 'placeholder': u'密码', 'required': ''}), label=u'密码')

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class LicenseForm(ModelForm):
    class Meta:
        model = Car
        fields = ('license',)


class CarForm(forms.Form):
    license = forms.CharField(max_length=50, label=u'车牌')
    cartype = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'select'}),
        choices=car_type_choice,
        label=u'选择车辆类型')


class UpdateForm(forms.Form):
    tickettype = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'select'}),
        choices=ticket_type_choice,
        label=u'选择要更改的包票类型')
