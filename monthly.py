import sys

sys.dont_write_bytecode = True
import argparse
import time
import datetime
from fs import write_data
from stock import Stock
from stocklist import StockList
from env import DefDateFmt, DefInterval
from log import Logger


def stocklist_update(l: list, nl: list, file, max, date, today, interval, force=False):
    max = len(l) if max == -1 else max
    for i, e in enumerate(nl[:max]):
        local = next((x for x in l if x["code"] == e["code"]), None)
        if local != None:
            lastdate = datetime.datetime.strptime(local["trade_date"], DefDateFmt).date()
            if not force and lastdate + datetime.timedelta(days=30) > today:
                Logger().info(f"[{i+1}/{max}] stock {e['code']} {e['name']} skipped, cause: less than 30 days passed from last update {lastdate}")
                continue
        o = Stock(e["code"], e["name"], e["market"], e["rdate"]).get_monthly(date)
        StockList.update_stock(l, o)
        Logger().info(f"[{i+1}/{max}] updating {o}")
        (i & 31 == 31) and write_data(l, file)  # incremental file save for a long period oper
        time.sleep(interval)  # reduce speed to avoid server block
    write_data(l, file)


def monthly_update(date: datetime.date = None, max=-1, interval=DefInterval, force=False):
    l = StockList()
    l.update()
    today = datetime.date.today()
    stocklist_update(l.shlist, l.nshlist, "shlist.txt", max, date, today, interval, force=force)
    stocklist_update(l.szlist, l.nszlist, "szlist.txt", max, date, today, interval, force=force)
    stocklist_update(l.bjlist, l.nbjlist, "bjlist.txt", max, date, today, interval, force=force)


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", default=None, help="end date")
    parser.add_argument("-n", "--number", type=int, default=-1, help="stock number")
    parser.add_argument("-i", "--interval", type=int, default=DefInterval, help="API call interval")
    parser.add_argument("-f", "--force", action="store_true", help="force to update, even if exists")
    args = parser.parse_args()
    Logger().info(f"args: {args}")
    return (args.number, args.date, args.interval, args.force)


if __name__ == "__main__":
    Logger().set_level(7).clear()
    (number, date, interval, force) = arg_parse()
    monthly_update(date=date, max=number, interval=interval, force=force)
