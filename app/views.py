from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, UpdateView
from .forms import CarForm, LicenseForm, UserForm
from .models import Ticket, Car, TicketType, CarType


# 车辆编辑视图
class CarUpdateView(UpdateView):
    model = Car
    fields = ['tickettype']
    def get_context_data(self, **kwargs):
        context = super(CarUpdateView, self).get_context_data(**kwargs)
        return context


# 车辆展示页
class CarListView(ListView):
    model = Car
    def get_context_data(self, **kwargs):
        context = super(CarListView, self).get_context_data(**kwargs)
        return context


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
                return HttpResponseRedirect('/AddCar')
            else:
                return HttpResponse(u"登陆失败")
        else:
            print(u"{0}, {1} 错误".format(username, password))
            return HttpResponse(u"用户名或密码错误")
    return render(request, 'user_login.html')


# 登出
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/UserLogin/')


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
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,
                  'register.html',
                  {'user_form':user_form,
                   'registered': registered})


#车辆包票服务
def add_ticket(request):
    pass


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
def find_by_license(max_results=0, starts_with=''):
    license_list = []
    if starts_with:
        license_list = Car.objects.filter(license__istartswith=starts_with)
#    if max_results > 0:
#        if len(license_list)> max_results:
#            license_list = license_list[:max_results]
    return license_list

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
