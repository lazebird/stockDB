import akshare as ak


class StockList:
    def __init__(self) -> None:
        self.shlst = StockList.get_shlst()
        self.szlst = StockList.get_szlst()
        self.bjlst = StockList.get_bjlst()

    def get_shlst():
        return ak.stock_info_sh_name_code(symbol="主板A股")

    def get_szlst():
        return ak.stock_info_sz_name_code(symbol="A股列表")

    def get_bjlst():
        return ak.stock_info_bj_name_code()

    def __repr__(self) -> str:
        return f"{{'sh': {self.shlst}, 'sz': {self.szlst}, 'bj': {self.bjlst}}}"
