from django.conf.urls import include, url
from django.contrib import admin
from app.views import add_car,\
    register, user_login, user_logout, car_in, car_out,\
    car_in_list, car_list, ticket_recode,\
    CarDetailView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', car_in_list, name='car-in-list'),
    url(r'^Car/CarOut/(?P<pk>\d+)/$', car_out, name='car-out'),
    url(r'^Car/CarIn/(?P<pk>\d+)/$', car_in, name='car-in'),
    url(r'^Car/TicketRecode/(?P<pk>\d+)/$', ticket_recode, name='ticket-recode'),
    url(r'^Car/Detail/(?P<pk>\d+)/$', CarDetailView.as_view(), name='car-detail'),
    url(r'^CarList/$', car_list, name='car-list'),
    url(r'^UserLogin/$', user_login, name='user-login'),
    url(r'^UserLogout/$', user_logout, name='user-logout'),
    url(r'^register/$', register, name='register'),
    url(r'^AddCar/$', add_car, name='add-car'),
]
