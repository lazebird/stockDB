import sys


sys.dont_write_bytecode = True
import akshare as ak
from fs import load_data
import datetime
from env import DefRDateFmt


class StockList:
    def __init__(self):
        (self.shlist, self.szlist, self.bjlist) = (load_data("shlist.txt", defval=[]), load_data("szlist.txt", defval=[]), load_data("bjlist.txt", defval=[]))

    def update(self):
        (self.nshlist, self.nszlist, self.nbjlist) = (StockList.get_shlist(), StockList.get_szlist(), StockList.get_bjlist())

    def get_shlist():
        return list(map(lambda d: {"code": d[0], "name": d[1], "market": "sh", "rdate": d[3]}, ak.stock_info_sh_name_code(symbol="主板A股").values))

    def get_szlist():
        return list(map(lambda d: {"code": d[1], "name": d[2], "market": "sz", "rdate": datetime.datetime.strptime(d[3], DefRDateFmt).date()}, ak.stock_info_sz_name_code(symbol="A股列表").values))

    def get_bjlist():
        return list(map(lambda d: {"code": d[0], "name": d[1], "market": "bj", "rdate": d[4]}, ak.stock_info_bj_name_code().values))

    def update_stock(l: list, n):
        (i, x) = next(((i, x) for i, x in enumerate(l) if x["code"] == n["code"]), (None, None))
        if i != None:
            del l[i]
        l.append(n)
        l.sort(key=lambda x: x["code"])

    def __repr__(self) -> str:
        return f"{self.shlist+self.szlist+self.bjlist}"


if __name__ == "__main__":
    # s = StockList()
    # print(s.shlist[:4])
    # print(s.szlist[:4])
    # print(s.bjlist[:4])
    print(ak.stock_info_sh_name_code(symbol="主板A股"))
    print(ak.stock_info_sz_name_code(symbol="A股列表"))
    print(ak.stock_info_bj_name_code())
