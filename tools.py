import sys


sys.dont_write_bytecode = True
import datetime
import json
import os
import argparse
from fs import load_data, write_xlsx, write_data, DataDir
from log import Logger
from stocklist import StockList
from tradedate import TradeDate
from env import DefDateFmt


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


def load_hisdirs():
    return list(map(lambda x: x.name, filter(lambda e: e.is_dir(), os.scandir(DataDir))))


def load_stock_hisdata(code, dirs: list[str]):
    datas = []
    for d in dirs:
        data = load_data(f"{d}/{code}.txt")
        data.pop("股票代码", 0)  # fix data attrs
        data != {} and datas.append(data)
    datas.sort(key=lambda x: x["日期"])
    return datas


def set_fund(e, name, suffixs: list, datas: list):
    if len(suffixs) != len(datas):
        Logger().err(f"stock {e['code']} {e['name']} suffixs len {len(suffixs)} and datas len {len(datas)} mismatch")
    lens = list(set(list(map(lambda d: len(d), datas))))  # data len should not be equal, remove duplicate len datas
    if len(lens) != len(datas):
        Logger().info(f"stock {e['code']} {e['name']} datas(len {len(datas)}) are not unique(unique len {len(lens)}), remove duplicated data")
    for i in range(len(lens)):  # use data len for data not enough case
        e[f"{name}-{suffixs[i]}"] = sum(list(map(lambda x: x[name], datas[i])))


def stock_x_xlsx(force):
    file = "output/X列表.xlsx"
    if not force and os.path.isfile(file):
        Logger().info(f"{file} write skipped, cause: already exists")
        return
    l = StockList()
    l = l.shlist + l.szlist + l.bjlist
    l.sort(key=lambda x: x["code"])
    dirs = load_hisdirs()
    tradedate = TradeDate()
    today = datetime.date.today()
    latest_tradedate = next(filter(lambda d: d >= today, tradedate.dlist))
    d5_ago = tradedate.dlist[tradedate.dlist.index(latest_tradedate) - 4]  # maybe overflow?
    d10_ago = tradedate.dlist[tradedate.dlist.index(latest_tradedate) - 9]  # maybe overflow?
    m1_ago = next(filter(lambda d: d >= (today - datetime.timedelta(days=30)), tradedate.dlist))
    m3_ago = next(filter(lambda d: d >= (today - datetime.timedelta(days=90)), tradedate.dlist))
    m6_ago = next(filter(lambda d: d >= (today - datetime.timedelta(days=180)), tradedate.dlist))
    y1_ago = next(filter(lambda d: d >= (today - datetime.timedelta(days=365)), tradedate.dlist))
    Logger().dbg(f"latest_tradedate {latest_tradedate}, d5_ago {d5_ago}, d10_ago {d10_ago}, m1_ago {m1_ago}, m3_ago {m3_ago}, m6_ago {m6_ago}, y1_ago {y1_ago}")
    for i, e in enumerate(l):
        # s = Stock(e["code"], e["name"], e["market"], e["rdate"])
        datas = load_stock_hisdata(e["code"], dirs)
        datas_5d = list(filter(lambda x: datetime.datetime.strptime(x["日期"], DefDateFmt).date() > d5_ago, datas))
        datas_10d = list(filter(lambda x: datetime.datetime.strptime(x["日期"], DefDateFmt).date() > d10_ago, datas))
        datas_1m = list(filter(lambda x: datetime.datetime.strptime(x["日期"], DefDateFmt).date() > m1_ago, datas))
        datas_3m = list(filter(lambda x: datetime.datetime.strptime(x["日期"], DefDateFmt).date() > m3_ago, datas))
        datas_6m = list(filter(lambda x: datetime.datetime.strptime(x["日期"], DefDateFmt).date() > m6_ago, datas))
        datas_1y = list(filter(lambda x: datetime.datetime.strptime(x["日期"], DefDateFmt).date() > y1_ago, datas))
        # calc price by latest, highest in 1y, lowest in 1y
        e["latest_price"] = datas[-1]["收盘"]
        e["highest_price_1y"] = max(list(map(lambda x: (x["最高"]), datas_1y)))
        e["lowest_price_1y"] = min(list(map(lambda x: (x["最低"]), datas_1y)))
        # calc fund flow by 5d 10d 1m 3m 6m 1y
        set_fund(e, "主力净流入-净额", ["5日", "10日", "1月", "3月", "6月", "1年"], [datas_5d, datas_10d, datas_1m, datas_3m, datas_6m, datas_1y])
        set_fund(e, "超大单净流入-净额", ["5日", "10日", "1月", "3月", "6月", "1年"], [datas_5d, datas_10d, datas_1m, datas_3m, datas_6m, datas_1y])
        set_fund(e, "大单净流入-净额", ["5日", "10日", "1月", "3月", "6月", "1年"], [datas_5d, datas_10d, datas_1m, datas_3m, datas_6m, datas_1y])
        set_fund(e, "中单净流入-净额", ["5日", "10日", "1月", "3月", "6月", "1年"], [datas_5d, datas_10d, datas_1m, datas_3m, datas_6m, datas_1y])
        set_fund(e, "小单净流入-净额", ["5日", "10日", "1月", "3月", "6月", "1年"], [datas_5d, datas_10d, datas_1m, datas_3m, datas_6m, datas_1y])
        Logger().info(f"[{i}/{len(l)}] collecting {e}")

    write_xlsx(l, file)


def stock_xlsx(name, force=False):
    l = StockList()
    l = list(filter(lambda x: str(x).find(name) != -1, l.shlist + l.szlist + l.bjlist))
    Logger().info(f"matched stocks: {list(map(lambda x:x['name'], l))}")
    dirs = load_hisdirs()
    for s in l:
        file = f"output/{s['name']}.xlsx"
        if not force and os.path.isfile(file):
            Logger().info(f"{file} write skipped, cause: already exists")
            continue
        datas = load_stock_hisdata(s["code"], dirs)
        write_xlsx(datas, file)


def data_check(start_date, end_date, days, force_remove=False):
    all_dirs: list[os.DirEntry[str]] = list(filter(lambda d: d.is_dir(), os.scandir(DataDir)))
    valid_dirs: list[os.DirEntry[str]] = []
    if start_date != None or end_date != None:
        valid_dirs = list(filter(lambda d: (start_date == None or d.name >= start_date) and (end_date == None or d.name <= end_date), all_dirs))
    else:
        lastdate = datetime.date.today() - datetime.timedelta(days=days)
        valid_dirs = list(filter(lambda d: datetime.datetime.fromtimestamp(os.path.getmtime(d.path)).date() > lastdate, all_dirs))
    invalid_dirs = list(map(lambda d: d.name, set(all_dirs).difference(valid_dirs)))
    invalid_dirs.sort()
    Logger().info(f"start_date {start_date}, end_date {end_date}, valid_dirs: {invalid_dirs}")
    for d in valid_dirs:
        fcnt = 0
        for f in os.scandir(d.path):
            fcnt = fcnt + 1
            with open(f.path, "r", encoding="utf8") as fp:
                o: dict[str, str] = json.load(fp)
                if o.get("日期", "").replace("/", "") != d.name:
                    Logger().err(f"file {f.path} data check error(remove={force_remove})")
                    force_remove and os.remove(f.path)
                    fcnt = fcnt - 1
        if fcnt == 0:
            Logger().err(f"dir {d.path} is empty(remove={force_remove})")
            force_remove and os.rmdir(d.path)


def arg_parse():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-m", "--mode", default="xlsx", help="split, stat, xlsx(default), check")
    parser.add_argument("-p", "--pe", type=int, default=50, help="pe value, used in stat mode")
    parser.add_argument("-t", "--pe_ttm", type=int, default=50, help="pe_ttm value, used in stat mode")
    parser.add_argument(
        "-n",
        "--names",
        default=None,
        nargs="+",
        help="""stock name pattern, used in xlsx mode. Examples: 
            'python tools.py -m xlsx 格力 美的' will get stocks's history datas that match with given pattern.
            'python tools.py -m xlsx' will get a list include all stocks""",
    )
    parser.add_argument("-f", "--force", action="store_true", help="force to update, even if exists")
    parser.add_argument("-s", "--start", help="start date, format %Y%m%d, used in check mode")
    parser.add_argument("-e", "--end", help="end date, format %Y%m%d, used in check mode")
    parser.add_argument("-d", "--days", type=int, default=1, help="how long days from today to check, default 1d, won't take effect if start/end date set, used in check mode")
    args = parser.parse_args()
    Logger().info(f"args: {args}")
    return (args.mode, args.pe, args.pe_ttm, args.names, args.force, args.start, args.end, args.days)


if __name__ == "__main__":
    Logger().set_level(7).clear()
    (mode, pe, pe_ttm, names, force, start, end, days) = arg_parse()
    match mode:
        case "split":
            split_stocklist()
        case "stat":
            stock_stat(pe, pe_ttm)
        case "xls" | "xlsx":
            stock_x_xlsx(force) if names == None else list(filter(lambda n: stock_xlsx(n, force), names))
        case "check":
            data_check(start, end, days, force)
