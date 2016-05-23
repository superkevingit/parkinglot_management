from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from .forms import CarForm, LicenseForm
from .models import Ticket, Car, TicketType, CarType
import json

# 输入车牌
def add_license(request):
    if request.method == 'POST':
        license_form = LicenseForm(request.POST)
        if license_form.is_valid():
            license = license_form.cleaned_data['license']
            HttpResponse.set_cookie("license", license)
            return HttpResponseRedirect(reverse('add-car'))
    else:
        license_form = LicenseForm()
    return render(request, 'find_by_license.html', {'license_form': license_form})


# 按车牌实时查找车辆
def find_by_license(request):
    license = request.GET['license']
    license_lists = Car.objects.filter(license__istartswith=license)
    license_json = []
    for license_list in license_lists:
        license_json.append(license_list.license)
    return HttpResponse(json.dumps(license_json), content_type='application/json')

# 添加车辆信息
def add_car(request):
    if request.method == 'POST':
        car_form = CarForm(request.POST, request.FILES)
        if car_form.is_valid():
            license = car_form.cleaned_data['license']
            car_type = car_form.cleaned_data['cartype']
            car_type = CarType.objects.get(id=car_type)
            exist_car = Car.objects.filter(license=license,
                                        cartype=car_type)
            if exist_car.exists():
                messages.add_message(request, messages.ERROR, u"car exist!")
                return HttpResponseRedirect(reverse('add-car'))
            else:
                new_car = Car(license=license,
                              cartype=car_type)
                new_car.save()
                messages.add_message(request, messages.SUCCESS, u"add car infomation success!")
                return HttpResponseRedirect(reverse('add-car'))
    else:
        car_form = CarForm()
    return render(request, 'add_car.html', {'car_form': car_form})
