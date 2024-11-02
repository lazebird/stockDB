import sys

sys.dont_write_bytecode = True
import time
import datetime
from fs import load_data, write_data
from stock import Stock
from env import DefDateFmt, DefInterval


def stock_update(lst: list, n):
    for i, s in enumerate(lst):
        if s["code"] == n["code"]:
            del lst[i]
    lst.append(n)
    lst.sort(key=lambda x: x["code"])


def daily_update(date: datetime.date = None, max=-1, interval=DefInterval):
    lst = load_data("list.txt", defval=[])
    for e in lst[:max]:
        print(e)
        s = Stock(e["code"], e["name"], e["market"])
        date = datetime.datetime.strptime(e["trade_date"], DefDateFmt).date()
        o = s.get_daily(start_date=date, end_date=date)
        time.sleep(interval)  # reduce speed to avoid server block
        write_data(o, "{}/{}.txt".format(date.strftime("%Y%m%d"), s.code))


if __name__ == "__main__":
    max = 4 if len(sys.argv) > 1 else -1
    daily_update(max=max)
