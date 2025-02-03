from czsc.gm_utils import *
from czsc.strategies import trader_strategy_a as strategy

os.environ['strategy_id'] = '31ebc3dc-08b1-11ec-a365-00d8619b544d'
os.environ['account_id'] = 'b95e8b9c9611b13143b81b303e288279976687fa'
os.environ['wx_key'] = '2daec96b-****-4f83-818b-2952fe2731c0'
os.environ['max_sym_pos'] = '0.5'
os.environ['path_gm_logs'] = 'C:/gm_logs'

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