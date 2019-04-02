# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tushare as ts
from osqa.conf import settings


def init_ts_pro_api():
    return ts.pro_api(settings.TUSHARE_PRO_TOKEN)


def get_stock_lists(ts_pro):
    pass


def get_daily_info_by_ts_code(ts_pro, start_date, end_date):
    pass
