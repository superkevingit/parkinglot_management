from django.conf.urls import include, url
from django.contrib import admin
from app.views import add_car, find_by_license, add_license

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^AddLicense/$', add_license, name='add-license'),
    url(r'^FindByLicense/$', find_by_license, name='find-by-license'),
    url(r'^AddCar/$', add_car, name='add-car'),
]
