# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime

from django.db import models


class Stock(models.Model):
    ts_code = models.CharField(max_length=128, default='', db_index=True)
    code = models.CharField(max_length=128, default='')
    name = models.CharField(max_length=128, default='')
    area = models.CharField(max_length=128, default='')
    industry = models.CharField(max_length=128, default='')
    market = models.CharField(max_length=128, default='')
    exchange = models.CharField(max_length=128, default='')
    status = models.CharField(max_length=128, default='')
    close_date = models.DateTimeField(default=datetime.datetime.fromtimestamp(0))
    is_hs = models.CharField(max_length=128, default='')


class StockDay(models.Model):
    stock = models.ForeignKey(Stock, related_name='stock_days', on_delete=models.CASCADE, db_index=True)
    trade_date = models.DateTimeField(default=datetime.datetime.fromtimestamp(0))
    pre_close = models.FloatField(blank=True, default=0.0, null=True)
    open = models.FloatField(blank=True, default=0.0, null=True)
    close = models.FloatField(blank=True, default=0.0, null=True)
    high = models.FloatField(blank=True, default=0.0, null=True)
    low = models.FloatField(blank=True, default=0.0, null=True)
    change = models.FloatField(blank=True, default=0.0, null=True)
    change_percentile = models.FloatField(blank=True, default=0.0, null=True)
    volume = models.FloatField(blank=True, default=0.0, null=True)
    amount = models.FloatField(blank=True, default=0.0, null=True)
