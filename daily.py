import os
import sys


sys.dont_write_bytecode = True
import time
import argparse
import datetime
from fs import get_datadir, load_data, write_data
from stock import Stock
from env import DefInterval, DefDateFmt
from stocklist import StockList
from log import Logger
from tradedate import TradeDate


def stock_update(tradedate: TradeDate, l: list, interval, date: datetime.date, force=False):
    max = len(l)
    for i, e in enumerate(l):
        s = Stock(e["code"], e["name"], e["market"], e["rdate"])
        if not tradedate.stock_check(s, date):
            Logger().err(f"stock {s.code} {s.name} skipped, cause: not trade in {date}")
            continue
        file = "{}/{}.txt".format(date.strftime("%Y%m%d"), s.code)
        if not force and load_data(file, {}) != {}:
            Logger().info(f"[{i+1}/{max}] stock {s.code} {s.name} {date} skipped, cause: {file} already exists")
            continue
        o = s.get_daily(start_date=date, end_date=date)
        time.sleep(interval)  # reduce speed to avoid server block
        write_data(o, file)
        Logger().info(f"[{i+1}/{max}] updating {o}")


def daily_update(tradedate: TradeDate, date: datetime.date = None, max=-1, interval=DefInterval, force=False):
    date = datetime.date.today() if date == None else date
    if not tradedate.date_check(date):
        return False
    l = StockList()
    stock_update(tradedate, l.shlist[:max], interval, date, force=force)
    stock_update(tradedate, l.szlist[:max], interval, date, force=force)
    stock_update(tradedate, l.bjlist[:max], interval, date, force=force)
    return True


def his_update(tradedate, end_date=datetime.date.today(), days=30, max=-1, interval=DefInterval, force=False):
    for i in range(days):
        date = end_date - datetime.timedelta(days=i)
        daily_update(tradedate, date=date, max=max, interval=interval, force=force)


def his_more(tradedate: TradeDate, end_date=datetime.date.today(), max=-1, interval=DefInterval, force=False):
    for i in range(365):
        date = end_date - datetime.timedelta(days=i)
        dir = get_datadir(date.strftime("%Y%m%d"))
        if os.path.isdir(dir) or not tradedate.date_check(date):
            continue
        daily_update(tradedate, date=date, max=max, interval=interval, force=force)
        break


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", default=datetime.date.today().strftime(DefDateFmt), help="end date")
    parser.add_argument("-n", "--number", type=int, default=-1, help="stock number")
    parser.add_argument("-l", "--long", type=int, default=1, help="days for history data")
    parser.add_argument("-i", "--interval", type=int, default=DefInterval, help="API call interval")
    parser.add_argument("-f", "--force", action="store_true", help="force to update, even if exists")
    parser.add_argument("-m", "--more", action="store_true", help="one more days's daily data, not exists now, not older than 365 days ago")
    args = parser.parse_args()
    Logger().info(f"args: {args}")
    return (args.number, args.date, args.long, args.interval, args.force, args.more)


if __name__ == "__main__":
    Logger().set_level(7).clear()
    (number, date, long, interval, force, more) = arg_parse()
    date = datetime.datetime.strptime(date, DefDateFmt).date()
    tradedate = TradeDate()
    more and his_more(tradedate, max=number, interval=interval, force=force)
    more or his_update(tradedate, end_date=date, days=long, max=number, interval=interval, force=force)
