# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime
import logging
import numpy as np
import data.ts_pro
from django.db.models import Q
from data.models import Stock, StockDay

logger = logging.getLogger('stock.data.utils')


def import_stock_basic():
    pro_api = data.ts_pro.init_ts_pro_api()
    df = data.ts_pro.get_stock_lists(pro_api)
    for index, row in df.iterrows():
        kwargs = {
            'ts_code': row['ts_code'],
            'code': row['symbol'],
            'name': row['name'],
            'area': row['area'],
            'industry': row['industry'],
            'market': row['market'],
            'exchange': row['exchange'],
            'status': row['list_status'],
            'is_hs': row['is_hs'],
        }
        Stock.objects.get_or_create(**kwargs)


def import_day_stocks():
    pro_api = data.ts_pro.init_ts_pro_api()
    stocks = Stock.objects.all()
    stock_count = stocks.count()
    count = 0
    for stock in stocks:
        print('stock code: %s' % stock.ts_code)
        df = data.ts_pro.get_daily_info_by_ts_code(pro_api, stock.ts_code)
        df_col = df.shape[1]
        for index, row in df.iterrows():
            kwargs = {
                'stock': stock,
                'trade_date': datetime.datetime.strptime(row['trade_date'], '%Y%m%d'),
                'pre_close': row['trade_date'],
                'open': row['open'] if not np.isnan(row['open']) else 0.0,
                'close': row['close'] if not np.isnan(row['close']) else 0.0,
                'high': row['high'] if not np.isnan(row['high']) else 0.0,
                'low': row['low'] if not np.isnan(row['low']) else 0.0,
                'change': row['change'] if not np.isnan(row['change']) else 0.0,
                'change_percentile': row['pct_chg'] if not np.isnan(row['pct_chg']) else 0.0,
                'volume': row['vol'] if not np.isnan(row['vol']) else 0.0,
                'amount': row['amount'] if not np.isnan(row['amount']) else 0.0,
                'ma_5': row['ma5'] if not np.isnan(row['ma5']) else 0.0,
                'ma_10': row['ma10'] if not np.isnan(row['ma10']) else 0.0,
                'ma_20': row['ma20'] if not np.isnan(row['ma20']) else 0.0,
                'ma_50': row['ma50'] if not np.isnan(row['ma50']) else 0.0,
                'ma_vol_5': row['ma_v_5'] if not np.isnan(row['ma_v_5']) else 0.0,
                'ma_vol_10': row['ma_v_10'] if not np.isnan(row['ma_v_10']) else 0.0,
                'ma_vol_20': row['ma_v_20'] if not np.isnan(row['ma_v_20']) else 0.0,
                'ma_vol_50': row['ma_v_50'] if not np.isnan(row['ma_v_50']) else 0.0,
            }
            StockDay.objects.get_or_create(**kwargs)
            print('stock %s imports daily trades at %d/%d' % (stock.code, index, df_col))
        count += 1
        print('day stocks imports at %d/%d' % (count, stock_count))


def revise_nan_ma_20_data():
    stockdays = StockDay.objects.filter(Q(ma_20=0.0) | Q(ma_vol_20=0.0))
    if stockdays.count() > 0:
        for stock_day in stockdays:
            ma_20, ma_v_20 = stock_day.revise_nan_avg_data()
            print(stock_day.ts_code, ma_20, ma_v_20)
