import sys


sys.dont_write_bytecode = True
import argparse
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


def stock_stat(pe, pe_ttm):
    l = StockList()
    Logger().info(f"shlist: {len(l.shlist)}, pe<{pe}, pe_ttm<{pe_ttm}: {len(list(filter(lambda x:x['pe_ttm']<pe_ttm and x['pe']<pe, l.shlist)))}")
    Logger().info(f"szlist: {len(l.szlist)}, pe<{pe}, pe_ttm<{pe_ttm}: {len(list(filter(lambda x:x['pe_ttm']<pe_ttm and x['pe']<pe, l.szlist)))}")
    Logger().info(f"bjlist: {len(l.bjlist)}, pe<{pe}, pe_ttm<{pe_ttm}: {len(list(filter(lambda x:x['pe_ttm']<pe_ttm and x['pe']<pe, l.bjlist)))}")


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", default="stat", help="split, stat")
    parser.add_argument("-p", "--pe", type=int, default=50, help="pe value")
    parser.add_argument("-t", "--pe_ttm", type=int, default=50, help="pe_ttm value")
    parser.add_argument("-s", "--force", action="store_true", help="force to update, even if exists")
    args = parser.parse_args()
    Logger().info(f"args: {args}")
    return (args.mode, args.pe, args.pe_ttm, args.force)


if __name__ == "__main__":
    (mode, pe, pe_ttm, force) = arg_parse()
    match mode:
        case "split":
            split_stocklist()
        case "stat":
            stock_stat(pe, pe_ttm)

# [2024-11-03 16:30:39][Info][tools.py:25] shlist: 1690, pe_ttm<50: 1000
# [2024-11-03 16:30:39][Info][tools.py:26] szlist: 2840, pe_ttm<50: 1274
# [2024-11-03 16:30:39][Info][tools.py:27] bjlist: 256, pe_ttm<50: 135
