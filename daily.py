import sys


sys.dont_write_bytecode = True
import time
import argparse
import datetime
from fs import load_data, write_data
from stock import Stock
from env import DefInterval, DefDateFmt
from stocklist import StockList
from log import Logger


def stock_update(l: list, max, interval, date, force=False):
    max = len(l) if max == -1 else max
    for i, e in enumerate(l[:max]):
        s = Stock(e["code"], e["name"], e["market"])
        file = "{}/{}.txt".format(date.strftime("%Y%m%d"), s.code)
        if not force and load_data(file, {}) != {}:
            Logger().info(f"[{i+1}/{max}] stock {s.code} {s.name} {date} skipped, cause: {file} already exists")
            continue
        o = s.get_daily(start_date=date, end_date=date)
        time.sleep(interval)  # reduce speed to avoid server block
        write_data(o, file)
        Logger().info(f"[{i+1}/{max}] updating {o}")


def daily_update(date: datetime.date = None, max=-1, interval=DefInterval, force=False):
    date = datetime.date.today() if date == None else date
    if date.weekday() > 4:
        Logger().err(f"no daily data in weekday {date.weekday()}, date {date}")
        return
    l = StockList()
    stock_update(l.shlist, max, interval, date, force=force)
    stock_update(l.szlist, max, interval, date, force=force)
    stock_update(l.bjlist, max, interval, date, force=force)


def his_update(end_date=datetime.date.today(), days=30, max=-1, interval=DefInterval, force=False):
    for i in range(days):
        date = end_date - datetime.timedelta(days=i)
        daily_update(date=date, max=max, interval=interval, force=force)


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", default=datetime.date.today().strftime(DefDateFmt), help="end date")
    parser.add_argument("-n", "--number", type=int, default=-1, help="stock number")
    parser.add_argument("-l", "--long", type=int, default=1, help="days for history data")
    parser.add_argument("-i", "--interval", type=int, default=DefInterval, help="API call interval")
    parser.add_argument("-f", "--force", action="store_true", help="force to update, even if exists")
    args = parser.parse_args()
    Logger().info(f"args: {args}")
    return (args.number, args.date, args.long, args.interval, args.force)


if __name__ == "__main__":
    Logger("output/daily.log").set_level(7).clear()
    (number, date, long, interval, force) = arg_parse()
    date = datetime.datetime.strptime(date, DefDateFmt).date()
    his_update(end_date=date, days=long, max=number, interval=interval, force=force)
