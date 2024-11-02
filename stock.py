import sys

sys.dont_write_bytecode = True
import datetime
import akshare as ak
import time


class Stock:
    def __init__(self, code, name, market):
        (self.code, self.name, self.market) = (code, name, market)
        self.indicator = self.hprice = self.fund_flow = None  # init for __repr__

    def get_monthly(self, date: datetime.date = None):
        indicator = self.indicator = Stock.get_indicator(self.code, date)
        if indicator == {}:  # too many reqs may fail?
            print(f"try again for code {self.code}, name {self.name} 3s later")
            time.sleep(3)
            indicator = self.indicator = Stock.get_indicator(self.code, date)

        indicator["trade_date"] = datetime.datetime.strftime(indicator.get("trade_date", datetime.date(1970, 1, 1)), "%Y/%m/%d")
        return {"code": self.code, "name": self.name, **indicator}

    def get_daily(self):
        today = datetime.datetime.today()
        self.hprice = Stock.get_hprice(self.code, start_date=(today - datetime.timedelta(days=1)).strftime("%Y%m%d"), end_date=today.strftime("%Y%m%d")).iloc[-1].to_dict()
        self.fund_flow = Stock.get_fund_flow(self.code, self.market)

    def get_indicator(code, date: datetime.date = None):
        i = {}
        indicators = None
        try:
            indicators = ak.stock_a_indicator_lg(symbol=code)
            i = indicators.iloc[-1].to_dict() if date == None else indicators[indicators["trade_date"] == date].iloc[-1].to_dict()
        except Exception as e:
            print(f"Error: code {code}, date {date}, indicators {indicators}, errmsg {e}")
        return i

    def get_hprice(code, start_date="20050501", end_date="20050520"):
        return ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")

    def get_fund_flow(code, market):
        return ak.stock_individual_fund_flow(stock=code, market=market).iloc[-1].to_dict()

    def __repr__(self) -> str:
        return f"{{{self.code, self.name, self.indicator, self.hprice, self.fund_flow}}}"


if __name__ == "__main__":
    s = Stock("000651", "格力电器", "sz")
    print(s.get_monthly())
