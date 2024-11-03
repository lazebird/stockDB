import sys

sys.dont_write_bytecode = True
from fs import load_data, write_data
from log import Logger


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


if __name__ == "__main__":
    split_stocklist()
