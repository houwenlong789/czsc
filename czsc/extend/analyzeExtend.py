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
        """
        初始中枢
        :return:
        """
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

            current_pen_price = low_price if low_price > 0 else high_price

            if last_center is not None and not last_center.has_confirm():
                # 判断是否破坏中枢, 低点在中枢上方
                up_break = current_bi.direction == Direction.Down and last_center.position_in_center(low_price) > 0

                # 判断是否破坏中枢，高点在中枢下方
                low_break = high_price is not None and last_center.position_in_center(high_price) < 0

                # 任何一个中枢破坏
                if up_break or low_break:
                    last_center.confirm_center()
                    # 回退一个判断
                    index -= 2
                    continue

            if last_center is not None and not last_center.has_confirm():
                last_center.list_bi.append(self.bi_list[index])
                index += 1
                continue

            if current_bi.direction == Direction.Down and not index + 2 >= bi_length:
                # 前置判断，是否是回调
                pre_check = self.bi_list[index + 2].low > self.bi_list[index].low
                if pre_check:
                    center_info = Center(bars=self.bi_list[index + 1:index + 5], direction=Direction.Down)
                    if center_info.is_valid_center():
                        self.center.append(center_info)
                        index += 5
                        if last_center is not None:
                            pre_main_center = last_center
                        last_center = center_info
                        continue

            # 回升
            if current_bi.direction == Direction.Up and not index + 2 >= bi_length:
                # 前置判断，是否是回升
                pre_check = self.bi_list[index + 2].high < self.bi_list[index].high
                if pre_check:
                    center_info = Center(bars=self.bi_list[index + 1:index + 5], direction=Direction.Down)
                    if center_info.is_valid_center():
                        self.center.append(center_info)

                    index += 5
                    last_center = center_info
                    if last_center is not None:
                        pre_main_center = last_center
                    continue

                    index += 1
                    if index >= line_length - 1:
                        break

            self.last_main_center = last_center
            self.pre_main_center = pre_main_center
