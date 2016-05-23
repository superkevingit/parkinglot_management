# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('license', models.CharField(max_length=50, unique=True, verbose_name='车牌')),
                ('status', models.BooleanField(default=False, verbose_name='是否在库')),
            ],
        ),
        migrations.CreateModel(
            name='CarType',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('car_type', models.CharField(max_length=20, choices=[('Teacher', '教职工车辆'), ('Social', '社会车辆'), ('Special', '公务车辆')], unique=True, verbose_name='车辆类型')),
            ],
        ),
        migrations.CreateModel(
            name='PortRecode',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('port_time', models.DateTimeField(auto_now_add=True, verbose_name='入库时间')),
                ('leave_time', models.DateTimeField(blank=True, null=True, verbose_name='出库时间')),
                ('charge', models.IntegerField(default=0, verbose_name='价格')),
                ('car', models.ForeignKey(to='app.Car')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('ticket_price', models.IntegerField(verbose_name='票价')),
                ('cartype', models.ForeignKey(to='app.CarType', verbose_name='车辆类型')),
            ],
        ),
        migrations.CreateModel(
            name='TicketRecode',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='开始时间')),
                ('stop_time', models.DateTimeField(verbose_name='停止时间')),
                ('car', models.ForeignKey(to='app.Car')),
                ('operator', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='操作者')),
            ],
        ),
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('ticket_type', models.CharField(max_length=20, choices=[('Hour', '小时票'), ('Month', '月票'), ('Quarter', '季度票'), ('Annual', '年票')], unique=True, verbose_name='购票类型')),
            ],
        ),
        migrations.AddField(
            model_name='ticketrecode',
            name='tickettype',
            field=models.ForeignKey(to='app.TicketType'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='tickettype',
            field=models.ForeignKey(to='app.TicketType', verbose_name='购票类型'),
        ),
        migrations.AddField(
            model_name='car',
            name='cartype',
            field=models.ForeignKey(to='app.CarType', verbose_name='车辆类型'),
        ),
        migrations.AddField(
            model_name='car',
            name='tickettype',
            field=models.ForeignKey(to='app.TicketType', verbose_name='车票类型', default=4),
        ),
    ]
