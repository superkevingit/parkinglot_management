#!/usr/bin/env python
# encoding: utf-8
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import CarType, Car


car_types = CarType.objects.all()
car_type_choice = []
for car_type in car_types:
    car_type_choice.append([car_type.id, car_type.car_type])


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

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
