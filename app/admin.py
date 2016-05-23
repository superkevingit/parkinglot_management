from django.contrib import admin
from .models import *

admin.site.register(Ticket)
admin.site.register(Car)
admin.site.register(TicketRecode)
admin.site.register(PortRecode)
admin.site.register(CarType)
admin.site.register(TicketType)
