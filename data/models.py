# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime
from django.db import models
import numpy as np
from sklearn.metrics import mean_squared_error


class Stock(models.Model):
    ts_code = models.CharField(max_length=128, default='', db_index=True)
    code = models.CharField(max_length=128, default='')
    name = models.CharField(max_length=128, default='')
    area = models.CharField(max_length=128, default='')
    industry = models.CharField(max_length=128, default='')
    market = models.CharField(max_length=128, default='')
    exchange = models.CharField(max_length=128, default='')
    status = models.CharField(max_length=128, default='')
    is_hs = models.CharField(max_length=128, default='')

    def to_dict(self):
        print({
            'id': self.id,
            'ts_code': self.ts_code,
            'code': self.code,
            'name': self.name,
            'area': self.area,
            'industry': self.industry,
            'market': self.market,
            'exchange': self.exchange,
            'status': self.status,
            'is_hs': self.is_hs,
             })


class StockDay(models.Model):
    stock = models.ForeignKey(Stock, related_name='stock_days', on_delete=models.CASCADE)
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

    #  avg close & vol (5, 10, 20, 50)
    ma_5 = models.FloatField(blank=True, default=0.0, null=True)
    ma_10 = models.FloatField(blank=True, default=0.0, null=True)
    ma_20 = models.FloatField(blank=True, default=0.0, null=True)
    ma_50 = models.FloatField(blank=True, default=0.0, null=True)

    ma_vol_5 = models.FloatField(blank=True, default=0.0, null=True)
    ma_vol_10 = models.FloatField(blank=True, default=0.0, null=True)
    ma_vol_20 = models.FloatField(blank=True, default=0.0, null=True)
    ma_vol_50 = models.FloatField(blank=True, default=0.0, null=True)

    # ratio of exchange: tor, ratio of vol: vr
    # ToDo---api in tushare pro is not ready to get these data for stock

    @property
    def ts_code(self):
        return self.stock.ts_code

    @property
    def code(self):
        return self.stock.code

    def to_dict(self):
        print({
            'ts_code': self.ts_code,
            'code': self.code,
            'trade_code': self.trade_date,
            'ma_5': self.ma_5,
            'ma_10': self.ma_10,
            'ma_20': self.ma_20,
            'ma_50': self.ma_50,
            'ma_vol_5': self.ma_vol_5,
            'ma_vol_10': self.ma_vol_10,
            'ma_vol_20': self.ma_vol_20,
            'ma_vol_50': self.ma_vol_50,
        })

    def revise_nan_avg_data(self, k=20):
        pre_stockdays = StockDay.objects.filter(stock__ts_code=self.ts_code, trade_date__lt=self.trade_date, trade_date__gte=(self.trade_date - datetime.timedelta(days=k)))
        close = pre_stockdays.values_list('close', flat=True).order_by('-trade_date')
        volume = pre_stockdays.values_list('volume', flat=True).order_by('-trade_date')
        ma = np.mean(close) if len(close) > 0 else 0.0
        ma_vol = np.mean(volume) if len(volume) > 0 else 0.0
        setattr(self, 'ma_%d' % k, ma)
        setattr(self, 'ma_vol_%d' % k, ma_vol)
        self.save(update_fields=['ma_%d' % k, 'ma_vol_%d' % k])
        return self.ma_20, self.ma_vol_20


class DayBoll(models.Model):
    daystock = models.OneToOneField(StockDay, related_name='day_boll', on_delete=models.CASCADE, db_index=True)

    # mean squared error md
    md_10 = models.FloatField(blank=True, default=0.0, null=True)
    md_20 = models.FloatField(blank=True, default=0.0, null=True)

    # boll mb
    mid_10 = models.FloatField(blank=True, default=0.0, null=True)
    mid_20 = models.FloatField(blank=True, default=0.0, null=True)

    # boll up
    upp_10 = models.FloatField(blank=True, default=0.0, null=True)
    upp_20 = models.FloatField(blank=True, default=0.0, null=True)

    # boll dn
    low_10 = models.FloatField(blank=True, default=0.0, null=True)
    low_20 = models.FloatField(blank=True, default=0.0, null=True)

    @property
    def stock(self):
        return self.daystock.stock

    @property
    def ts_code(self):
        return self.daystock.ts_code

    @property
    def code(self):
        return self.daystock.code

    @property
    def trade_date(self):
        return self.daystock.trade_date

    @property
    def pre_day_stock(self):
        if not all([self.ts_code, self.trade_date]):
            return None
        pre_trade_date = self.trade_date - datetime.timedelta(days=1)
        pre_day_stock = self.stock.stock_days.filter(trade_date=pre_trade_date)
        if pre_day_stock.count() != 1:
            return None
        return pre_day_stock

    @property
    def pre_10_day_stocks(self):
        if not all([self.ts_code, self.trade_date]):
            return []
        pre_10_trade_date = self.trade_date - datetime.timedelta(days=10)
        return self.stock.stock_days.filter(trade_date__lt=self.trade_date, trade_date__gte=pre_10_trade_date)

    @property
    def pre_20_day_stocks(self):
        if not all([self.ts_code, self.trade_date]):
            return []
        pre_20_trade_date = self.trade_date - datetime.timedelta(days=20)
        return self.stock.stock_days.filter(trade_date__lt=self.trade_date, trade_date__gte=pre_20_trade_date)

    def to_dict(self):
        pass

    def set_mid(self):
        if self.pre_day_stock is not None:
            self.mid_10 = self.pre_day_stock.ma_10
            self.mid_20 = self.pre_day_stock.ma_20
            self.save(update_fields=['mid_10', 'mid_20'])

    def set_md_10(self):
        pre_10_zip_list = [(item.close, item.ma_10) for item in self.pre_10_day_stocks if (item is not None and isinstance(item, StockDay))]
        pre_10_unzip_list = zip(*pre_10_zip_list)
        pre_10_close = pre_10_unzip_list[0]
        pre_10_ma = pre_10_unzip_list[1]
        md = mean_squared_error(pre_10_close, pre_10_ma)
        self.md_10 = md
        self.save(update_fields=['md_10'])

    def set_md_20(self):
        pre_20_zip_list = [(item.close, item.ma_20) for item in self.pre_20_day_stocks if (item is not None and isinstance(item, StockDay))]
        pre_20_unzip_list = zip(*pre_20_zip_list)
        pre_20_close = pre_20_unzip_list[0]
        pre_20_ma = pre_20_unzip_list[1]
        md = mean_squared_error(pre_20_close, pre_20_ma)
        self.md_20 = md
        self.save(update_fields=['md_20'])

    def upp_10(self, k=1.5):
        return self.mid_10 + k * self.md_10

    def upp_20(self, k=2):
        return self.mid_20 + k * self.md_20

    def low_10(self, k=1.5):
        return self.mid_10 - k * self.md_10

    def low_20(self, k=2):
        return self.mid_20 - k * self.md_20
