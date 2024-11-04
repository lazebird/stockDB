import sys

sys.dont_write_bytecode = True
import datetime
from fs import load_data, write_data
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


def stock_update(lst: list, n):
    for i, s in enumerate(lst):
        if s["code"] == n["code"]:
            del lst[i]
    lst.append(n)
    lst.sort(key=lambda x: x["code"])


def func_test():
    lst = load_data("list.txt", defval=[])
    for e in StockList().lst:
        s = Stock(e["code"], e["name"], e["market"], e["rdate"])
        o = s.get_monthly(datetime.date(2024, 11, 1))
        stock_update(lst, o)
    write_data(lst, "list.txt")


def line_test():
    print(f"akshare version={ak.__version__}")
    stock_a_indicator_lg_df = ak.stock_a_indicator_lg(symbol=code_geli)
    # avail_date = stock_a_indicator_lg_df.tail(1)["trade_date"].values[0]
    # print(stock_a_indicator_lg_df[stock_a_indicator_lg_df["trade_date"] == avail_date])
    # print(stock_a_indicator_lg_df.iloc[-1].to_dict())
    print(ak.stock_individual_fund_flow(stock=code_geli, market="sh"))


if __name__ == "__main__":
    # line_test()
    # list_test()
    func_test()
