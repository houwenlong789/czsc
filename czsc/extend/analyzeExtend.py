from czsc import CZSC
from czsc.objects import *
from czsc.extend.center import Center


class CZSCExtend(CZSC):
    def __init__(self, bars: List[RawBar], freq: str, max_bi_count=30):
        super(CZSCExtend, self).__init__(bars, freq, max_bi_count)
        self.center: List[Center] = []
        self.last_main_center: Center = None
        self.pre_main_center: Center = None

    def build_init_main_center(self):
        bi_length = len(self.bi_list)
        if bi_length < 6:
            return

        last_center: Center = None
        pre_main_center: Center = None
        index = 0
        while index < bi_length - 1:
            # 向上方向判断,并判断当前是否满足向上的中枢(回调)
            # index = 0 表示向上一个线段低点
            low_price = self.bi_list[index].low
            high_price = self.bi_list[index].high
            current_bi = self.bi_list[index]

            current_pen_price = low_price if low_price>0 else high_price

            if current_bi.direction == Direction.Down and not index+2>=bi_length:
                # 前置判断，是否是回调
                pre_check = self.bi_list[index+2].low > self.bi_list[index].low
                if pre_check:
                    center_info = Center(bars=self.bi_list[index+1:index+5], direction=Direction.Down)



