import sys


sys.dont_write_bytecode = True
import datetime
import akshare as ak
from env import DefDateFmt, DefRDateFmt
from log import Logger


class Stock:
    def __init__(self, code, name, market, rdate):
        (self.code, self.name, self.market) = (code, name, market)
        self.rdate = datetime.datetime.strptime(rdate, DefRDateFmt).date() if isinstance(rdate, str) else rdate
        self.indicator = self.hprice = self.fund_flow = None  # init for __repr__

    def get_monthly(self, start_date: datetime.date = None, end_date: datetime.date = datetime.date.today()) -> list[dict]:
        indicator = self.indicator = Stock.get_indicator(self.code, start_date, end_date)
        res = []
        for e in indicator:
            d = {
                **{"code": self.code, "name": self.name, "market": self.market, "rdate": datetime.datetime.strftime(self.rdate, DefRDateFmt), "trade_date": datetime.datetime.strftime(e.get("trade_date", datetime.date(1970, 1, 1)), DefDateFmt)},
                **{k: v for k, v in e.items() if not k in ["trade_date"]},
            }
            res.append(d)
        return res

    def get_daily(self, start_date: datetime.date = datetime.date.today(), end_date: datetime.date = datetime.date.today()) -> list[dict]:
        if end_date < self.rdate:
            return {}
        start_date = self.rdate if start_date < self.rdate else start_date
        hprice = self.hprice = Stock.get_hprice(self.code, start_date=start_date.strftime("%Y%m%d"), end_date=end_date.strftime("%Y%m%d"))
        fund_flow = self.fund_flow = Stock.get_fund_flow(self.code, self.market, start_date, end_date)
        res = []
        for i in range(0, min(len(hprice), len(fund_flow))):
            d = {
                **{"code": self.code, "name": self.name, "market": self.market, **fund_flow[i], "日期": datetime.datetime.strftime(hprice[i].get("日期", datetime.date(1970, 1, 1)), DefDateFmt)},
                **{k: v for k, v in {**hprice[i], **fund_flow[i]}.items() if not k in ["日期", "股票代码"]},
            }
            res.append(d)
        return res

    def get_indicator(code, start_date: datetime.date, end_date: datetime.date) -> list[dict]:
        dt = ak.stock_a_indicator_lg(symbol=code)
        dt = dt if start_date == None else dt[(dt["trade_date"] >= start_date) & (dt["trade_date"] <= end_date)]
        l = list(map(lambda t: t[1].to_dict(), dt.iterrows()))
        return l

    def get_hprice(code, start_date="20240201", end_date="20240204") -> list[dict]:
        dt = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
        if dt.empty:
            Logger().err(f"code {code}, start_date {start_date}, end_date {end_date}, dt.empty {dt.empty}")
            return []
        l = list(map(lambda t: t[1].to_dict(), dt.iterrows()))
        return l

    def get_fund_flow(code, market, start_date: datetime.date, end_date: datetime.date) -> list[dict]:
        dt = ak.stock_individual_fund_flow(stock=code, market=market)  # last half year data only
        dt = dt if start_date == None else dt[(dt["日期"] >= start_date) & (dt["日期"] <= end_date)]
        if dt.empty:
            Logger().err(f"code {code}, start_date {start_date}, end_date {end_date}, dt.empty {dt.empty}")
            return []
        l = list(map(lambda t: t[1].to_dict(), dt.iterrows()))
        return l

    def __repr__(self) -> str:
        return f"{{{self.code, self.name, self.indicator, self.hprice, self.fund_flow}}}"


if __name__ == "__main__":
    s = Stock("000651", "格力电器", "sz", "1996-11-18")
    # Logger().info(s.get_monthly(datetime.datetime.strptime("20240201", "%Y%m%d").date(), datetime.datetime.strptime("20240204", "%Y%m%d").date()))
    # Logger().info(Stock.get_hprice(s.code, start_date="20240201", end_date="20240204"))
    # Logger().info(s.get_daily(start_date=datetime.datetime.strptime("20240601", "%Y%m%d").date(), end_date=datetime.datetime.strptime("20240604", "%Y%m%d").date()))
