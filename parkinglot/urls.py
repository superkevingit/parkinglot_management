from django.conf.urls import include, url
from django.contrib import admin
from app.views import add_car, ticket_list

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^add_car/$', add_car, name='add-car'),
    url(r'^ticket_list/(.*)$', ticket_list, name='ticket-list'),
]
