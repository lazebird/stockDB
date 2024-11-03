import sys

sys.dont_write_bytecode = True
import time
import datetime
from fs import write_data
from stock import Stock
from stocklist import StockList
from env import DefDateFmt, DefInterval
from log import Logger


def stocklist_update(l: list, nl: list, file, max, date, today, interval):
    max = len(l) if max == -1 else max
    for i, e in enumerate(l[:max]):
        local = next((x for x in l if x["code"] == e["code"]), None)
        if local != None:
            lastdate = datetime.datetime.strptime(local["trade_date"], DefDateFmt).date()
            if lastdate + datetime.timedelta(days=30) > today:
                Logger().info(f"[{i+1}/{max}] stock {e['code']} {e['name']} skipped, cause: less than 30 days passed from last update {lastdate}")
                continue
        o = Stock(e["code"], e["name"], e["market"]).get_monthly(date)
        StockList.update_stock(l, o)
        Logger().info(f"[{i+1}/{max}] updating {o}")
        write_data(l, file)  # incremental file save for a long period oper
        time.sleep(interval)  # reduce speed to avoid server block
    write_data(l, file)


def monthly_update(date: datetime.date = None, max=-1, interval=DefInterval):
    l = StockList()
    l.update()
    today = datetime.date.today()
    stocklist_update(l.shlist, l.nshlist, "shlist.txt", max, date, today, interval)
    stocklist_update(l.szlist, l.nszlist, "szlist.txt", max, date, today, interval)
    stocklist_update(l.bjlist, l.nbjlist, "bjlist.txt", max, date, today, interval)


if __name__ == "__main__":
    max = 4 if len(sys.argv) > 1 else -1
    monthly_update(max=max)
