import sys


sys.dont_write_bytecode = True
import datetime
import time
import akshare as ak
from env import DefDateFmt, DefRDateFmt
from log import Logger


class Stock:
    def __init__(self, code, name, market, rdate):
        (self.code, self.name, self.market) = (code, name, market)
        self.rdate = datetime.datetime.strptime(rdate, DefRDateFmt).date() if isinstance(rdate, str) else rdate
        self.indicator = self.hprice = self.fund_flow = None  # init for __repr__

    def get_monthly(self, date: datetime.date = None):
        indicator = self.indicator = Stock.get_indicator(self.code, date)
        if indicator == {}:  # too many reqs may fail?
            Logger().err(f"try again for code {self.code}, name {self.name} 3s later")
            time.sleep(3)
            indicator = self.indicator = Stock.get_indicator(self.code, date)

        indicator["trade_date"] = datetime.datetime.strftime(indicator.get("trade_date", datetime.date(1970, 1, 1)), DefDateFmt)
        return {"code": self.code, "name": self.name, "market": self.market, "rdate": datetime.datetime.strftime(self.rdate, DefRDateFmt), **indicator}

    def get_daily(self, start_date: datetime.date = datetime.date.today(), end_date: datetime.date = datetime.date.today()):
        if end_date < self.rdate:
            return {}
        start_date = self.rdate if start_date > self.rdate else start_date
        hprice = self.hprice = Stock.get_hprice(self.code, start_date=start_date.strftime("%Y%m%d"), end_date=end_date.strftime("%Y%m%d"))
        fund_flow = self.fund_flow = Stock.get_fund_flow(self.code, self.market, end_date)
        fund_flow["日期"] = datetime.datetime.strftime(fund_flow.get("日期", datetime.date(1970, 1, 1)), DefDateFmt)
        return {"code": self.code, "name": self.name, "market": self.market, **hprice, **fund_flow}

    def get_indicator(code, date: datetime.date = None):
        i = {}
        dt = None
        try:
            dt = ak.stock_a_indicator_lg(symbol=code)
            i = dt.iloc[-1].to_dict() if date == None else dt[dt["trade_date"] == date].iloc[-1].to_dict()
        except Exception as e:
            Logger().err(f"Error: code {code}, date {date}, indicators {dt}, errmsg {e}")
        return i

    def get_hprice(code, start_date="20050501", end_date="20050520"):
        dt = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
        if dt.empty:
            Logger().err(f"code {code}, start_date {start_date}, end_date {end_date}, dt.empty {dt.empty}")
            return {}
        return dt.iloc[-1].to_dict()

    def get_fund_flow(code, market, date):
        dt = ak.stock_individual_fund_flow(stock=code, market=market)
        dt = dt if date == None else dt[dt["日期"] == date]
        if dt.empty:
            Logger().err(f"code {code}, date {date}, dt.empty {dt.empty}")
            return {}
        return dt.iloc[-1].to_dict()

    def __repr__(self) -> str:
        return f"{{{self.code, self.name, self.indicator, self.hprice, self.fund_flow}}}"


if __name__ == "__main__":
    s = Stock("000651", "格力电器", "sz", "1996-11-18")
    Logger().info(s.get_monthly())
