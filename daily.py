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


def stock_update(tradedate: TradeDate, l: list, interval, start_date: datetime.date, end_date: datetime.date, force=False):
    max = len(l)
    for i, e in enumerate(l):
        s = Stock(e["code"], e["name"], e["market"], e["rdate"])
        if not tradedate.stock_check(s, start_date):
            Logger().err(f"stock {s.code} {s.name} skipped, cause: not trade in {start_date}")
            continue
        datas = s.get_daily(start_date=start_date, end_date=end_date)
        time.sleep(interval)  # reduce speed to avoid server block
        for d in datas:
            file = "{}/{}.txt".format(d.get("日期", "1970/01/01").replace("/", ""), s.code)
            if not force and load_data(file, {}) != {}:
                Logger().info(f"[{i+1}/{max}] stock {s.code} {s.name} skipped, cause: {file} already exists")
                continue
            write_data(d, file)
            Logger().info(f"[{i+1}/{max}] updating file {file}, data {d}")


def daily_update(tradedate: TradeDate, start_date: datetime.date, end_date: datetime.date, max=-1, interval=DefInterval, force=False):
    start_date = datetime.date.today() if start_date == None else start_date
    end_date = datetime.date.today() if end_date == None else end_date
    if not tradedate.date_check(start_date):
        return False
    l = StockList()
    stock_update(tradedate, l.shlist[:max] + l.szlist[:max] + l.bjlist[:max], interval, start_date=start_date, end_date=end_date, force=force)
    return True


def his_update(tradedate, end_date=datetime.date.today(), days=30, max=-1, interval=DefInterval, force=False):
    date = end_date - datetime.timedelta(days=days)
    daily_update(tradedate, start_date=date, end_date=end_date, max=max, interval=interval, force=force)


def his_more(tradedate: TradeDate, end_date=datetime.date.today(), max=-1, interval=DefInterval, force=False):
    for i in range(365):
        date = end_date - datetime.timedelta(days=i)
        dir = get_datadir(date.strftime("%Y%m%d"))
        if os.path.isdir(dir) or not tradedate.date_check(date):
            continue
        daily_update(tradedate, start_date=date - datetime.timedelta(days=30), end_date=date, max=max, interval=interval, force=force)
        break


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", default=datetime.date.today().strftime(DefDateFmt), help="end date")
    parser.add_argument("-n", "--number", type=int, default=-1, help="stock number")
    parser.add_argument("-l", "--long", type=int, default=30, help="days for history data")
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
    more and his_more(tradedate, end_date=date, max=number, interval=interval, force=force)
    more or his_update(tradedate, end_date=date, days=long, max=number, interval=interval, force=force)
