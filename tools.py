import sys


sys.dont_write_bytecode = True
from fs import load_data, write_data
from log import Logger
from stocklist import StockList


def split_stocklist():
    lst: list = load_data("list.txt", defval=[])
    shlist = list(filter(lambda x: x["market"] == "sh", lst))
    szlist = list(filter(lambda x: x["market"] == "sz", lst))
    bjlist = list(filter(lambda x: x["market"] == "bj", lst))
    write_data(shlist, "shlist.txt")
    write_data(szlist, "szlist.txt")
    write_data(bjlist, "bjlist.txt")
    Logger().info(f"write {len(shlist)} stocks to  shlist.txt")
    Logger().info(f"write {len(szlist)} stocks to  szlist.txt")
    Logger().info(f"write {len(bjlist)} stocks to  bjlist.txt")


def stock_stat():
    l = StockList()
    Logger().info(f"shlist: {len(l.shlist)}, pe_ttm<50: {len(list(filter(lambda x:x['pe_ttm']<50, l.shlist)))}")
    Logger().info(f"szlist: {len(l.szlist)}, pe_ttm<50: {len(list(filter(lambda x:x['pe_ttm']<50, l.szlist)))}")
    Logger().info(f"bjlist: {len(l.bjlist)}, pe_ttm<50: {len(list(filter(lambda x:x['pe_ttm']<50, l.bjlist)))}")


if __name__ == "__main__":
    # split_stocklist()
    stock_stat()

# [2024-11-03 16:30:39][Info][tools.py:25] shlist: 1690, pe_ttm<50: 1000
# [2024-11-03 16:30:39][Info][tools.py:26] szlist: 2840, pe_ttm<50: 1274
# [2024-11-03 16:30:39][Info][tools.py:27] bjlist: 256, pe_ttm<50: 135
