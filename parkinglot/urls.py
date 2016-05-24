from django.conf.urls import include, url
from django.contrib import admin
from app.views import add_car, find_by_license, add_license,\
    register, user_login, user_logout,\
    CarListView, CarDetailView, CarUpdateView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^Car/Update/(?P<pk>\d+)/$', CarUpdateView.as_view(), name='car-update'),
    url(r'^Car/Detail/(?P<pk>\d+)/$', CarDetailView.as_view(), name='car-detail'),
    url(r'^Car/$', CarListView.as_view(), name='car-list'),
    url(r'^UserLogin/$', user_login, name='user-login'),
    url(r'^UserLogOut/$', user_logout, name='user-logout'),
    url(r'^register/$', register, name='register'),
    url(r'^AddLicense/$', add_license, name='add-license'),
    url(r'^FindByLicense/$', find_by_license, name='find-by-license'),
    url(r'^AddCar/$', add_car, name='add-car'),
]
