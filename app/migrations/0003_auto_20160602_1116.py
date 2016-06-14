# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20160525_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='tickettype',
            field=models.ForeignKey(to='app.TicketType', default=1, verbose_name='车票类型'),
        ),
    ]
