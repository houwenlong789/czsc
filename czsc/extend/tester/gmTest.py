
from czsc.gm_utils import *

def test_gm_set_token():
    set_gm_token("b95e8b9c9611b13143b81b303e288279976687fa")

def test_set_enviroment():
    os.environ['strategy_id'] = '475a918b-e9f9-11ec-becd-00d8619b544d'
    os.environ['account_id'] = '1db0ec26-08b1-11ec-a731-00163e0a4100'
    os.environ['wx_key'] = '2daec96b-****-4f83-818b-2952fe2731c0'
    os.environ['max_sym_pos'] = '0.5'
    os.environ['path_gm_logs'] = 'd:/gm_logs'