from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView
from .forms import CarForm, LicenseForm, UserForm, UpdateForm
from .models import Ticket, Car, TicketType, CarType, PortRecode, TicketRecode
from datetime import *


# 车辆入库
def car_in(request, pk):
    car = Car.objects.get(id=pk)
    if car:
        if not car.status:
            Car.objects.filter(id=pk).update(status=True)
            PortRecode.objects.create(car=car, port_time=datetime.now())
            messages.add_message(request, messages.SUCCESS, u"车辆成功入库")
            return HttpResponseRedirect(reverse('car-detail', args=(pk,)))
        else:
            messages.add_message(request, messages.WARNING, u"车辆已经在库中")
            return HttpResponseRedirect(reverse('car-detail', args=(pk,)))
    return HttpResponseRedirect(reverse('car-list'))

# 车辆出库
def car_out(request, pk):
    leave_time = datetime.now()
    car = Car.objects.get(id=pk)
    if car:
        if car.status:
            ticket = Ticket.objects.get(cartype=car.cartype, tickettype=car.tickettype)
            portrecode = PortRecode.objects.get(car=car, leave_time=None)
            if ticket and portrecode:
                charge = ticket.calculate_charge(ticket_type=car.tickettype.ticket_type, port_time=portrecode.port_time, leave_time=leave_time)
                portrecode.leave_time = leave_time
                portrecode.charge = charge
                portrecode.save
                Car.objects.filter(id=pk).update(status=False)
                messages.add_message(request, messages.SUCCESS, u"车辆成功出库")
                return HttpResponseRedirect(reverse('car-detail', args=(pk,)))
            else:
                messages.add_message(request, messages.WARNING, u"出库失败")
                return HttpResponseRedirect(reverse('car-detail', args=(pk,)))
        else:
            messages.add_message(request, messages.WARNING, u"库内无此车")
            return HttpResponseRedirect(reverse('car-list'))
    return HttpResponseRedirect(reverse('car-list'))



# 车辆包票
def ticket_recode(request, pk):
    tickets = Ticket.objects.all()
    car = Car.objects.filter(id=pk)
    _car = Car.objects.get(id=pk)
    if request.method == 'POST':
        update_form = UpdateForm(data=request.POST)
        if update_form.is_valid():
            tickettype=update_form.cleaned_data['tickettype']
            _tickettype=TicketType.objects.get(id=tickettype)
            start_time, stop_time = TicketRecode.get_ticket_period(ticket_type=_tickettype.ticket_type)
            operator = request.user
            TicketRecode.objects.update_or_create(car=_car, tickettype=_tickettype,
                                        start_time=start_time,
                                        stop_time=stop_time,
                                        operator=operator)
            car.update(tickettype=_tickettype)
            messages.add_message(request, messages.SUCCESS, u"包票成功！")
            return HttpResponseRedirect(reverse('car-detail', args=(pk,)))
    else:
        update_form = UpdateForm()
    return render(request, 'app/ticket_recode.html',
                  {'tickets': tickets, 'car': car, 'update_form':update_form})


# 库内车辆展示
def car_in_list(request):
    port_car = PortRecode.objects.select_related('car').order_by('port_time').filter(leave_time=None).reverse()
    return render(request, 'car_in_list.html', {'port_car': port_car})

# 全部车辆展示
def  car_list(request):
    cars = Car.objects.all()
    return render(request, 'app/car_list.html', {'cars': cars})

# 车辆详情
class CarDetailView(DetailView):
    model = Car
    def get_context_data(self, **kwargs):
        context = super(CarDetailView, self).get_context_data(**kwargs)
        return context


# 登陆
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('add-car'))
            else:
                return HttpResponse(u"登陆失败")
        else:
            print(u"{0}, {1} 错误".format(username, password))
            return HttpResponse(u"用户名或密码错误")
    return render(request, 'user_login.html')


# 登出
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user-login'))


# 注册
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            return HttpResponseRedirect(reverse('add-car'))
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,
                  'register.html',
                  {'user_form':user_form,
                   'registered': registered})


# 添加车辆信息
def add_car(request):
    if request.method == 'POST':
        car_form = CarForm(request.POST, request.FILES)
        if car_form.is_valid():
            license = car_form.cleaned_data['license']
            car_type = car_form.cleaned_data['cartype']
            car_type = CarType.objects.get(id=car_type)
            exist_car = Car.objects.filter(license=license)
            if exist_car.exists():
                for car in exist_car:
                    pk = car.id
                messages.add_message(request, messages.WARNING, u"该车已存在")
                return HttpResponseRedirect(reverse('car-detail', args=(pk,)))
            else:
                new_car = Car(license=license,
                              cartype=car_type)
                new_car.save()
                messages.add_message(request, messages.SUCCESS, u"添加车辆成功")
                return HttpResponseRedirect(reverse('car-list'))
    else:
        car_form = CarForm()
    return render(request, 'add_car.html', {'car_form': car_form})
