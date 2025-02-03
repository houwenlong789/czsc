from czsc.gm_utils  import *
from datetime import datetime
import locale

def test_set_my_token():
    os.environ['strategy_id'] = '31ebc3dc-08b1-11ec-a365-00d8619b544d'
    os.environ['account_id'] = 'b95e8b9c9611b13143b81b303e288279976687fa'
    os.environ['wx_key'] = '2daec96b-****-4f83-818b-2952fe2731c0'
    os.environ['max_sym_pos'] = '0.5'
    os.environ['path_gm_logs'] = 'C:/gm_logs'

    os.environ["strategy_id"]


def test_change_local():

    locale.setlocale(locale.LC_CTYPE, 'chinese')
    nt=datetime.now()
    print(nt.strftime('%Y年%m月%d日 %H时%M分%S秒'))
