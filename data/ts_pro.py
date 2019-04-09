# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf import settings

import pandas as ps
import tushare as ts


def init_ts_pro_api():
    ts.set_token(settings.TUSHARE_PRO_TOKEN)
    return ts.pro_api()


def get_stock_lists(ts_pro):
    return ts_pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,market,exchange,list_status,is_hs')


def get_daily_info_by_ts_code(ts_pro, ts_code, start_date='20181201', end_date='20190404'):
    if start_date == '':
        start_date = '20181201'
    if end_date == '':
        end_date = ps.datetime.today().strftime('%Y%m%d')
    return ts.pro_bar(api=ts_pro, asset='E', ts_code=ts_code, start_date=start_date, end_date=end_date, ma=[5, 10, 20, 50])
