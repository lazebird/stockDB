import sys

sys.dont_write_bytecode = True
import time
import datetime
from fs import load_data, write_data
from stock import Stock
from stocklist import StockList


def stock_update(lst: list, n):
    for i, s in enumerate(lst):
        if s["code"] == n["code"]:
            del lst[i]
    lst.append(n)
    lst.sort(key=lambda x: x["code"])


def monthly_update(date: datetime.date = None, max=-1, interval=5):
    lst = load_data("list.txt", defval=[])
    for e in StockList().lst[:max]:
        s = Stock(e["code"], e["name"], e["market"])
        o = s.get_monthly(date)
        stock_update(lst, o)
        time.sleep(interval)  # reduce speed to avoid server block
    write_data(lst, "list.txt")


if __name__ == "__main__":
    max = 4 if len(sys.argv) > 1 else -1
    monthly_update(max=max)
