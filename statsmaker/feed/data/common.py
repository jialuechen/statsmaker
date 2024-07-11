import requests
import re
import akshare as ak
import pandas as pd
import datetime
from llmbroker.util import *


class MARKET:
    SH = 'SH'
    SZ = 'SZ'
    BJ = 'BJ'


g_market_list = [MARKET.SH, MARKET.SZ, MARKET.BJ]


class MARKETID:
    SH = 1
    SZ = 2
    BJ = 3


class STOCKTYPE:
    BLOCK = 0  
    A = 1  
    INDEX = 2  
    B = 3  
    FUND = 4  
    ETF = 5  
    ND = 6 
    BOND = 7  
    GEM = 8  
    START = 9  


def get_stktype_list(quotations=None):
    
    if not quotations:
        return (1, 2, 3, 4, 5, 6, 7, 8, 9)

    result = []
    for quotation in quotations:
        new_quotation = quotation.lower()
        if new_quotation == 'stock':
            result += [STOCKTYPE.A, STOCKTYPE.INDEX, STOCKTYPE.B, STOCKTYPE.GEM, STOCKTYPE.START]
        elif new_quotation == 'fund':
            result += [STOCKTYPE.FUND, STOCKTYPE.ETF]
        elif new_quotation == 'bond':
            result += [STOCKTYPE.ND, STOCKTYPE.BOND]
        else:
            print('Unknow quotation: {}'.format(quotation))

    return tuple(result)


@llmbroker_catch(ret=[], trace=True)
def get_stk_code_name_list(market: str) -> list:
    if market == MARKET.SZ:
        ind_list = ["A股列表", "B股列表"]
        df = None
        for ind in ind_list:
            tmp_df = ak.stock_info_sz_name_code(ind)
            tmp_df.rename(columns={'A股代码': 'code', 'A股简称': 'name'}, inplace=True)
            df = pd.concat([df, tmp_df]) if df is not None else tmp_df
        llmbroker_info("获取深圳证券交易所股票数量: {}", len(df) if df is not None else 0)
        return df[['code', 'name']].to_dict(orient='records') if df is not None else []

    if market == MARKET.SH:
        ind_list = ["主板A股", "主板B股", "科创板"]
        df = None
        for ind in ind_list:
            tmp_df = ak.stock_info_sh_name_code(ind)
            tmp_df.rename(columns={'证券代码': 'code', '证券简称': 'name'}, inplace=True)
            df = pd.concat([df, tmp_df]) if df is not None else tmp_df
        llmbroker_info("获取上海证券交易所股票数量: {}", len(df) if df is not None else 0)
        return df[['code', 'name']].to_dict(orient='records') if df is not None else []

   
    if market == MARKET.BJ:
        df = ak.stock_info_bj_name_code()
        df.rename(columns={'证券代码': 'code', '证券简称': 'name'}, inplace=True)
        llmbroker_info("获取北京证券交易所股票数量: {}", len(df) if df is not None else 0)
        return df[['code', 'name']].to_dict(orient='records') if df is not None else []


@llmbroker_catch(ret=[], trace=True)
def get_index_code_name_list() -> list:
    
    df = ak.stock_zh_index_spot()
    return [{'market_code': df.loc[i]['代码'].upper(), 'name': df.loc[i]['名称']} for i in range(len(df))]


g_fund_code_name_list = {}
for market in g_market_list:
    g_fund_code_name_list[market] = []
g_last_get_fund_code_name_list_date = datetime.date(1990, 12, 9)


@llmbroker_catch(ret=[], trace=True)
def get_fund_code_name_list(market: str) -> list:
    
    global g_last_get_fund_code_name_list_date
    now = datetime.date.today()
    if now <= g_last_get_fund_code_name_list_date:
        return g_fund_code_name_list[market]

    ind_list = "封闭式基金", "ETF基金", "LOF基金"
    for ind in ind_list:
        df = ak.fund_etf_category_sina(ind)
        for i in range(len(df)):
            loc = df.loc[i]
            try:
                code, name = str(loc['代码']), str(loc['名称'])
                g_fund_code_name_list[code[:2].upper()].append(dict(code=code[2:], name=name))
            except Exception as e:
                llmbroker_error("{}! {}", str(e), loc)
    llmbroker_info("获取基金列表数量: {}", len(g_fund_code_name_list[market]))
    g_last_get_fund_code_name_list_date = now
    return g_fund_code_name_list[market]


@llmbroker_catch(ret=[], trace=True)
def get_new_holidays():
    
    res = requests.get('https://www.tdx.com.cn/url/holiday/')
    res.encoding = res.apparent_encoding
    ret = re.findall(r'<textarea id="data" style="display:none;">([\s\w\d\W]+)</textarea>', res.text, re.M)[0].strip()
    day = [d.split('|')[:4] for d in ret.split('\n')]
    return [v[0] for v in day if v[2] == 'China']