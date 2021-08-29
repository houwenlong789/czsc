# coding: utf-8
"""
基于聚宽数据的实时日线因子监控
"""

# 首次使用需要设置聚宽账户
# from czsc.data.jq import set_token
# set_token("phone number", 'password') # 第一个参数是JQData的手机号，第二个参数是登录密码
import traceback
import time
import shutil
import os
from datetime import datetime
# from czsc.data.jq import JqCzscTrader as CzscTrader
from czsc.objects import Signal, Factor, Event, Operate
from czsc.utils.io import read_pkl, save_pkl
from czsc.extend.utils import push_text
from czsc.extend.tdx import TdxStoreage, Market, get_kline
from czsc.extend.analyzeExtend import CZSCExtendTrader as CzscTrader

# =======================================================================================================
# 基础参数配置
ct_path = os.path.join("d:\\data", "czsc_traders")
os.makedirs(ct_path, exist_ok=True)

symbols = ["600763.XSHG", "600031.XSHG", "603958.XSHG"]

qywx_key = ""

my_dic_container = {}


def monitor(use_cache=True):
    moni_path = os.path.join(ct_path, "monitorTdx")
    os.makedirs(moni_path, exist_ok=True)
    events_monitor = [
        # 开多
        Event(name="一买", operate=Operate.LO, factors=[
            Factor(name="5分钟类一买", signals_all=[Signal("5分钟_倒1笔_类买卖点_类一买_任意_任意_0")]),
            Factor(name="5分钟形一买", signals_all=[Signal("5分钟_倒1笔_基础形态_类一买_任意_任意_0")]),

            Factor(name="15分钟类一买", signals_all=[Signal("15分钟_倒1笔_类买卖点_类一买_任意_任意_0")]),
            Factor(name="15分钟形一买", signals_all=[Signal("15分钟_倒1笔_基础形态_类一买_任意_任意_0")]),

            Factor(name="30分钟类一买", signals_all=[Signal("30分钟_倒1笔_类买卖点_类一买_任意_任意_0")]),
            Factor(name="30分钟形一买", signals_all=[Signal("30分钟_倒1笔_基础形态_类一买_任意_任意_0")]),
        ]),

        Event(name="二买", operate=Operate.LO, factors=[
            Factor(name="5分钟类二买", signals_all=[Signal("5分钟_倒1笔_类买卖点_类二买_任意_任意_0")]),
            Factor(name="5分钟形二买", signals_all=[Signal("5分钟_倒1笔_基础形态_类二买_任意_任意_0")]),

            Factor(name="15分钟类二买", signals_all=[Signal("15分钟_倒1笔_类买卖点_类二买_任意_任意_0")]),
            Factor(name="15分钟形二买", signals_all=[Signal("15分钟_倒1笔_基础形态_类二买_任意_任意_0")]),

            Factor(name="30分钟类二买", signals_all=[Signal("30分钟_倒1笔_类买卖点_类二买_任意_任意_0")]),
            Factor(name="30分钟形二买", signals_all=[Signal("30分钟_倒1笔_基础形态_类二买_任意_任意_0")]),
        ]),
        Event(name="三买", operate=Operate.LO, factors=[
            Factor(name="5分钟类三买", signals_all=[Signal("5分钟_倒1笔_类买卖点_类三买_任意_任意_0")]),
            Factor(name="5分钟形三买", signals_all=[Signal("5分钟_倒1笔_基础形态_类三买_任意_任意_0")]),

            Factor(name="15分钟类三买", signals_all=[Signal("15分钟_倒1笔_类买卖点_类三买_任意_任意_0")]),
            Factor(name="15分钟形三买", signals_all=[Signal("15分钟_倒1笔_基础形态_类三买_任意_任意_0")]),

            Factor(name="30分钟类三买", signals_all=[Signal("30分钟_倒1笔_类买卖点_类三买_任意_任意_0")]),
            Factor(name="30分钟形三买", signals_all=[Signal("30分钟_倒1笔_基础形态_类三买_任意_任意_0")]),
        ]),

        # 平多
        Event(name="一卖", operate=Operate.LE, factors=[
            Factor(name="5分钟类一卖", signals_all=[Signal("5分钟_倒1笔_类买卖点_类一卖_任意_任意_0")]),
            Factor(name="5分钟形一卖", signals_all=[Signal("5分钟_倒1笔_基础形态_类一卖_任意_任意_0")]),

            Factor(name="15分钟类一卖", signals_all=[Signal("15分钟_倒1笔_类买卖点_类一卖_任意_任意_0")]),
            Factor(name="15分钟形一卖", signals_all=[Signal("15分钟_倒1笔_基础形态_类一卖_任意_任意_0")]),

            Factor(name="30分钟类一卖", signals_all=[Signal("30分钟_倒1笔_类买卖点_类一卖_任意_任意_0")]),
            Factor(name="30分钟形一卖", signals_all=[Signal("30分钟_倒1笔_基础形态_类一卖_任意_任意_0")]),
        ]),
        Event(name="二卖", operate=Operate.LE, factors=[
            Factor(name="5分钟类二卖", signals_all=[Signal("5分钟_倒1笔_类买卖点_类二卖_任意_任意_0")]),
            Factor(name="5分钟形二卖", signals_all=[Signal("5分钟_倒1笔_基础形态_类二卖_任意_任意_0")]),

            Factor(name="15分钟类二卖", signals_all=[Signal("15分钟_倒1笔_类买卖点_类二卖_任意_任意_0")]),
            Factor(name="15分钟形二卖", signals_all=[Signal("15分钟_倒1笔_基础形态_类二卖_任意_任意_0")]),

            Factor(name="30分钟类二卖", signals_all=[Signal("30分钟_倒1笔_类买卖点_类二卖_任意_任意_0")]),
            Factor(name="30分钟形二卖", signals_all=[Signal("30分钟_倒1笔_基础形态_类二卖_任意_任意_0")]),
        ]),
        Event(name="三卖", operate=Operate.LE, factors=[
            Factor(name="5分钟类三卖", signals_all=[Signal("5分钟_倒1笔_类买卖点_类三卖_任意_任意_0")]),
            Factor(name="5分钟形三卖", signals_all=[Signal("5分钟_倒1笔_基础形态_类三卖_任意_任意_0")]),

            Factor(name="15分钟类三卖", signals_all=[Signal("15分钟_倒1笔_类买卖点_类三卖_任意_任意_0")]),
            Factor(name="15分钟形三卖", signals_all=[Signal("15分钟_倒1笔_基础形态_类三卖_任意_任意_0")]),

            Factor(name="30分钟类三卖", signals_all=[Signal("30分钟_倒1笔_类买卖点_类三卖_任意_任意_0")]),
            Factor(name="30分钟形三卖", signals_all=[Signal("30分钟_倒1笔_基础形态_类三卖_任意_任意_0")]),
        ]),
    ]
    for s in symbols:
        current_date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        print("{}.{}".format(s, current_date_str))
        try:

            ct = CzscTrader(s, max_count=1000, freq_list=None)
            # 每次执行，会在moni_path下面保存一份快照
            file_html = os.path.join(moni_path, f"{ct.symbol}_{ct.end_dt.strftime('%Y%m%d%H%M')}.html")
            ct.take_snapshot(file_html, width="1400px", height="580px")

            msg = f"标的代码：{s} {current_date_str} \n同花顺F10：http://basic.10jqka.com.cn/{s.split('.')[0]}\n"
            for event in events_monitor:
                m, f = event.is_match(ct.s)
                key = "{}{}".format(s, f)
                print(key)
                if m:
                    result = my_dic_container.get(key, None)
                    if result is None:
                        msg += "监控提醒：{}@{}\n".format(event.name, f)
                        my_dic_container[key] = 1

            if "监控提醒" in msg:
                push_text(msg.strip("\n"), key=qywx_key)

        except Exception as e:
            traceback.print_exc()
            print("{} 执行失败 - {}".format(s, e))


def run_monitor():
    mdt = ["09:30", "09:41", "09:51", "10:00", "10:30", "11:00", "11:20", "13:00", "13:30", "14:00", "14:01", "14:06",
           "14:16", "14:26",
           "14:30", "14:50", "18:25", "18:28"]
    monitor()
    while 1:
        print(datetime.now().strftime("%H:%M"))
        if datetime.now().strftime("%H:%M") in mdt:
            monitor()
        time.sleep(3)


if __name__ == '__main__':
    run_monitor()