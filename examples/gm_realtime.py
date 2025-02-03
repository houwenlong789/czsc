# -*- coding: utf-8 -*-
"""
author: zengbin93
email: zeng_bin8888@163.com
create_dt: 2021/12/13 17:48
describe: A股股票实盘仿真

环境变量设置说明：
strategy_id                 掘金研究策略ID
account_id                  账户ID
wx_key                      企业微信群聊机器人Key
max_sym_pos                 单仓位限制
path_gm_logs                gm_logs的路径，默认值：C:/gm_logs

环境变量设置样例：
# 使用 os 模块设置

"""

from czsc.gm_utils import *
from czsc.strategies import trader_strategy_a as strategy

# os.environ['strategy_id'] = '475a918b-e9f9-11ec-becd-00d8619b544d'
# os.environ['account_id'] = '1db0ec26-08b1-11ec-a731-00163e0a4100'
# os.environ['wx_key'] = '2daec96b-****-4f83-818b-2952fe2731c0'
# os.environ['max_sym_pos'] = '0.5'
# os.environ['path_gm_logs'] = 'd:/gm_logs'

def init(context):
    symbols = [
        'SZSE.300014',
        'SHSE.600143',
        'SZSE.002216',
        'SZSE.300033',
        'SZSE.000795',
        'SZSE.002739',
        'SHSE.600000',
        'SHSE.600008',
        'SHSE.600006',
        'SHSE.600009',
        'SHSE.600010',
        'SHSE.600011'
    ]
    name = f"{strategy.__name__}"
    init_context_universal(context, name)
    init_context_env(context)
    init_context_traders(context, symbols, strategy)
    init_context_schedule(context)


if __name__ == '__main__':
    run(filename=os.path.basename(__file__), token=gm_token, mode=MODE_LIVE, strategy_id=os.environ['strategy_id'])

