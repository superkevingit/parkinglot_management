from django.db import models
from django.contrib.auth.models import User
from datetime import *
from dateutil.relativedelta import *

# 车辆类型
class CarType(models.Model):
    CAR_TYPE_CHOICES = (
        ('Teacher', u'教职工车辆'),
        ('Social', u'社会车辆'),
        ('Special', u'公务车辆'),
    )
    car_type = models.CharField(u'车辆类型',
                                max_length=20,
                                choices=CAR_TYPE_CHOICES)
    def __str__(self):
        return u'%s' % self.car_type


# 车票类型
class TicketType(models.Model):
    TICKET_TYPE_CHOICES =(
        ('Month', u'月票'),
        ('Quarter', u'季度票'),
        ('Annual', u'年票'),
        ('Hour', u'小时票'),
    )
    ticket_type = models.CharField(u'票类型', max_length=20,
                                   choices=TICKET_TYPE_CHOICES)

    def __str__(self):
        return u'%s' % self.ticket_type

# 车票价格
class Ticket(models.Model):
    cartype = models.ForeignKey('CarType')
    tickettype = models.ForeignKey('TicketType')
    ticket_price = models.IntegerField(u'票价')

    def __str__(self):
        return u'%s %s' % (self.cartype, self.tickettype)


# 车辆信息
class Car(models.Model):
    license = models.CharField(u'车牌', max_length=50)
    cartype = models.ForeignKey('CarType')
    tickettype = models.ForeignKey('TicketType')
    status = models.BooleanField(u'是否在库', default=False)

    def __str__(self):
        return u'%s' % self.license


# 包票记录
class TicketRecode(models.Model):
    car = models.ForeignKey('Car')
    tickettype = models.ForeignKey('TicketType')
    start_time = models.DateTimeField(u"开始时间")
    stop_time = models.DateTimeField(u"停止时间")
    operator = models.ForeignKey(User)

    def __str__(self):
        return u'%s %s' % (self.car.license, self.ticket.ticket_type)

    def get_ticket_period(self, ticket_type):
        begin = datetime.now()
        end = begin+calculate_stop(begin, ticket_type)
        return begin, end

    def calculate_stop_time(self, begin, ticket_type):
        if ticket_type == 'Month':
            stop_time = begin+relativedelta(months=+1)
            return stop_time
        elif ticket_type == 'Quarter':
            stop_time = begin+relativedelta(months=+3)
            return stop_time
        elif ticket_type == 'Annual':
            stop_time = begin+relativedelta(years=+1)
            return stop_time
        else:
            stop_time = begin+relativedelta(hours=+1)
            return stop_time


# 泊车记录
class PortRecode(models.Model):
    car = models.ForeignKey('Car')
    port_time = models.DateTimeField(u"入库时间", auto_now_add=True)
    leave_time = models.DateTimeField(u"出库时间",
                                      null=True, blank=True)
    charge = models.IntegerField(u"价格", default=0)
