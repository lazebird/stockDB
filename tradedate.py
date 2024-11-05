import sys


sys.dont_write_bytecode = True
import datetime
import akshare as ak
from stock import Stock


class TradeDate:
    def __init__(self):
        self.dlist: list[datetime.date] = list(map(lambda x: x[0], ak.tool_trade_date_hist_sina().values))  # 从 1990-12-19 到 2024-12-31 之间的股票交易日历数据

    def date_check(self, date: datetime.date):
        return date in self.dlist

    def stock_check(self, s: Stock, date: datetime.date):
        return False if (not date in self.dlist or date < s.rdate) else True
