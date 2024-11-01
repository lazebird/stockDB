import sys

sys.dont_write_bytecode = True
import akshare as ak
from stock import Stock
from stocklist import StockList

code_geli = "000651"


def list_test():
    # print(ak.stock_info_sh_name_code(symbol="主板A股").values[0])
    # print(ak.stock_info_sz_name_code(symbol="A股列表").values[0])
    # print(ak.stock_info_bj_name_code().values[0])
    l = StockList()
    print(l)


def func_test():
    s = Stock(code_geli, "格力电器")
    print(s)


def line_test():
    print(f"akshare version={ak.__version__}")
    stock_a_indicator_lg_df = ak.stock_a_indicator_lg(symbol=code_geli)
    # avail_date = stock_a_indicator_lg_df.tail(1)["trade_date"].values[0]
    # print(stock_a_indicator_lg_df[stock_a_indicator_lg_df["trade_date"] == avail_date])
    # print(stock_a_indicator_lg_df.iloc[-1].to_dict())
    print(ak.stock_individual_fund_flow(stock=code_geli, market="sh"))


if __name__ == "__main__":
    # line_test()
    # func_test()
    list_test()
