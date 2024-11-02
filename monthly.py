import sys

sys.dont_write_bytecode = True
import time
import datetime
from fs import load_data, write_data
from stock import Stock
from stocklist import StockList
from env import DefDateFmt, DefInterval
from log import Logger


def stock_update(lst: list, n):
    (i, x) = next(((i, x) for i, x in enumerate(lst) if x["code"] == n["code"]), (None, None))
    if i != None:
        del lst[i]
    lst.append(n)
    lst.sort(key=lambda x: x["code"])


def monthly_update(date: datetime.date = None, max=-1, interval=DefInterval):
    lst: list = load_data("list.txt", defval=[])
    nlst = StockList().lst
    max = len(nlst) if max == -1 else max
    today = datetime.date.today()
    for i, e in enumerate(nlst[:max]):
        local = next((x for x in lst if x["code"] == e["code"]), None)
        if local != None:
            lastdate = datetime.datetime.strptime(local["trade_date"], DefDateFmt).date()
            if lastdate + datetime.timedelta(days=30) > today:
                Logger().info(f"stock {e['code']} {e['name']} skipped, cause: less than 30 days passed from last update {lastdate}")
                continue
        o = Stock(e["code"], e["name"], e["market"]).get_monthly(date)
        stock_update(lst, o)
        Logger().info(f"[{i+1}/{max}] updating {o}")
        time.sleep(interval)  # reduce speed to avoid server block
    write_data(lst, "list.txt")


if __name__ == "__main__":
    max = 4 if len(sys.argv) > 1 else -1
    monthly_update(max=max)
