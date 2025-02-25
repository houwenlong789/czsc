# coding: utf-8
"""
目前 czsc 库处于开发阶段，不同版本之间的 API 兼容性较差。
这个文件对应的 czsc 版本为 0.7.3，代码即文档，关于0.7.3的所有你想知道的都在代码里。

注意：czsc 是针对程序化实盘进行设计的，用来做研究需要自己按需求改动代码，强烈建议研究、实盘使用统一的代码。
"""

import czsc
# 聚宽数据为目前支持的数据源，需要接入第三方数据源的请参考这个文件进行编写

import traceback
from datetime import datetime
import pandas as pd
from typing import List
from czsc.analyze import CZSC
from czsc.signals.signals import get_default_signals, get_selector_signals
from czsc.data.jq import get_index_stocks
from czsc.objects import Signal, Factor
from czsc.extend.tdx import TdxStoreage, Market, get_kline
from czsc.extend.utils import read_csv_symbol



# ======================================================================================================================
# 使用单个级别的信号进行选股

def is_third_buy_W(symbol):
    """判断一个股票现在是否有日线三买"""
    bars = get_kline(symbol, end_date='', freq="W", count=200)
    c = CZSC(bars, get_signals=get_default_signals)

    factor_ = Factor(
        name="类三买选股因子",
        signals_any=[
            Signal("周线_倒1笔_基础形态_类二买_任意_任意_0"),
            Signal("周线_倒1笔_类买卖点_类二买_任意_任意_0"),
        ],
        signals_all=[
        ]
    )
    if factor_.is_match(c.signals):
        c.open_in_browser()
        return True
    else:
        return False


def two_buy_day(symbol):
    """判断一个股票现在是否有日线三买"""
    bars = get_kline(symbol, end_date='', freq="D", count=800)
    c = CZSC(bars, get_signals=get_default_signals)

    factor_ = Factor(
        name="类二买选股因子",
        signals_any=[
            Signal("日线_倒1笔_基础形态_类二买_任意_任意_0"),
            Signal("日线_倒1笔_类买卖点_类二买_任意_任意_0"),
        ],
        signals_all=[
        ]
    )

    if factor_.is_match(c.signals):
        c.open_in_browser()
        return True
    else:
        return False


def is_day_bc(symbol):
    """
     判断是否背驰
     :param symbol:
     :return:
     """
    bars = get_kline(symbol, freq="D", end_date=datetime.now(), count=1000)
    c = CZSC(bars, get_signals=get_selector_signals)

    factor_ = Factor(
        name="背驰选股",
        signals_any=[
            Signal("日线_倒1笔_三笔形态_向下盘背_任意_任意_0"),
            Signal("日线_倒1笔_基础形态_底背驰_任意_任意_0")
        ],
        signals_all=[
            # Signal("30分钟_倒0笔_潜在三买_构成中枢_任意_任意_0")
        ]
    )
    if factor_.is_match(c.signals):
        c.open_in_browser()
        return True
    else:
        return False

def is_week_bc(symbol):
    bars = get_kline(symbol, freq="W", end_date=datetime.now(), count=1000)
    c = CZSC(bars, get_signals=get_selector_signals)

    factor_ = Factor(
        name="背驰选股",
        signals_any=[
            Signal("周线_倒1笔_三笔形态_向下盘背_任意_任意_0"),
            Signal("周线_倒1笔_基础形态_底背驰_任意_任意_0"),
        ],
        signals_all=[
            # Signal("30分钟_倒0笔_潜在三买_构成中枢_任意_任意_0")
        ]
    )
    # c.open_in_browser()
    if factor_.is_match(c.signals):
        return True
    else:
        return False


def is_bc(symbol):
    """
    判断是否背驰
    :param symbol:
    :return:
    """
    bars = get_kline(symbol, freq="30min", end_date=datetime.now(), count=1000)
    c = CZSC(bars, get_signals=get_selector_signals)

    factor_ = Factor(
        name="背驰选股",
        signals_any=[
            Signal("30分钟_倒1笔_三笔形态_向下盘背_任意_任意_0"),
            Signal("30分钟_倒1笔_基础形态_底背驰_任意_任意_0"),
            Signal("30分钟_倒1笔_类买卖点_类一买_任意_任意_0"),
            Signal("30分钟_倒1笔_类买卖点_类二买_任意_任意_0"),
        ],
        signals_all=[
            # Signal("30分钟_倒0笔_潜在三买_构成中枢_任意_任意_0")
        ]
    )
    # c.open_in_browser()
    if factor_.is_match(c.signals):
        return True
    else:
        return False


def run_jq_selector():
    # 获取上证50最新成分股列表，这里可以换成自己的股票池
    symbols: List = get_index_stocks("399008.XSHE")
    #symbols, dic = read_csv_symbol("d:/data/Table.csv")
    only_three_buy: List = []
    bc_buy: List = []
    for symbol in symbols:
        try:
            print("{} start".format(symbol))
            if is_week_bc(symbol):
                print("{} - 二买".format(symbol))
                only_three_buy.append(symbol)

        except:
            print("{} - 执行失败".format(symbol))
            traceback.print_exc()
    print(only_three_buy)
    print(bc_buy)
    print("end")


if __name__ == '__main__':
    run_jq_selector()
