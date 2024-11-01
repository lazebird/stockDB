import akshare as ak


class StockList:
    def __init__(self):
        self.shlst = StockList.get_shlst()
        self.szlst = StockList.get_szlst()
        self.bjlst = StockList.get_bjlst()

    def get_shlst():
        return list(map(lambda d: {"code": d[0], "name": d[1], "market": "sh"}, ak.stock_info_sh_name_code(symbol="主板A股").values))

    def get_szlst():
        return list(map(lambda d: {"code": d[1], "name": d[2], "market": "sz"}, ak.stock_info_sz_name_code(symbol="A股列表").values))

    def get_bjlst():
        return list(map(lambda d: {"code": d[0], "name": d[1], "market": "bj"}, ak.stock_info_bj_name_code().values))

    def __repr__(self) -> str:
        return f"{{'sh': {self.shlst}, 'sz': {self.szlst}, 'bj': {self.bjlst}}}"
