import datetime
import akshare as ak


class Stock:
    def __init__(self, code, name):
        self.basic = {"code": code, "name": name}
        self.indicator = Stock.get_indicator(code)
        today = datetime.datetime.today()
        self.hprice = Stock.get_hprice(code, start_date=(today - datetime.timedelta(days=1)).strftime("%Y%m%d"), end_date=today.strftime("%Y%m%d")).iloc[-1].to_dict()
        self.fund_flow = Stock.get_fund_flow(code)

    def get_indicator(code):
        indicators = ak.stock_a_indicator_lg(symbol=code)
        return indicators.iloc[-1].to_dict()

    def get_hprice(code, start_date="20050501", end_date="20050520"):
        return ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")

    def get_fund_flow(code, market="sz"):
        return ak.stock_individual_fund_flow(stock=code, market=market).iloc[-1].to_dict()

    def __repr__(self) -> str:
        return f"{{{self.basic, self.indicator, self.hprice, self.fund_flow}}}"
