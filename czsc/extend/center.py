from enum import Enum
from czsc.objects import *
from typing import List


class CenterFrom(Enum):
    """
    中枢构成的方式
    """
    # 原始数据构造
    ORIGIN = 1
    # 中枢扩张
    CENTER_EXPAND = 2
    # 中枢延伸
    CENTER_STRETCH = 3

class TrendType(Enum):
    """
    两个中枢构成的类型
    """
    # 上升
    RISE = 0
    # 下跌
    FALL = 1
    # 更大的趋势
    BIG_CENTER = 2



class Center:
    """
    中枢信息
    """

    @property
    def zg(self):
        if self.direction == Direction.Up:
            return min(self.list_bi[0].high,
                       self.list_bi[2].high)
        else:
            return min(self.list_bi[1].high,
                       self.list_bi[3].high)

    @property
    def zd(self):
        if self.direction == Direction.UP:
            return max(self.list_bi[1].low,
                       self.list_bi[3].low)
        else:
            return max(self.list_bi[0].low,
                       self.list_bi[2].low)

    def __init__(self, bars: List[BI], direction: Direction,
                 source: CenterFrom = CenterFrom.ORIGIN,
                 main_center=None, expand_center=None,
                 level: int = 0):
        # 原始数据
        self.list_bi = bars

        # 中枢构建方式
        self.source: CenterFrom = source
        # 中枢方向
        self.direction = direction
        # 级别
        self.level = level
        # 核心中枢
        self.main_center: Center = main_center
        # 扩张 中枢
        self.expand_center: Center = expand_center

        # 中枢是否破坏
        self.__confirm = False

    def has_confirm(self):
        return self.__confirm

    # def compare_center(self, center):
    #     """
    #     比较两个中枢
    #     :param center: 后一个中枢
    #     :return: 返回两个中枢的趋势
    #     """
    #     has_same_range = self.zd <= center.zg <= self.zg or self.zd <= center.zd <= self.zg
    #     if has_same_range:
    #         return consts.trend_none
    #     if center.zd > self.zg:
    #         return consts.trend_up
    #     if center.zg < self.zd:
    #         return consts.trend_down
    #     return consts.trend_none

    def position_in_center(self, compare_price):
        """
        判断在中枢的位置  1  上  0 中  -1 下
        :param compare_price:
        :return:
        """
        if compare_price > self.zg:
            return 1
        if compare_price < self.zd:
            return -1
        return 0

    def trend_style(self, line_gg, line_dd):
        """
        判断趋势类型
        """
        has_same_range = self.dd <= line_dd <= self.gg or self.dd <= self.gg
        if has_same_range:
            return TrendType.BIG_CENTER

        if line_dd > self.gg:
            return TrendType.RISE
        if line_gg < self.dd:
            return TrendType.FALL
        raise RuntimeError('请检查趋势逻辑')

    def confirm_center(self):
        """
        确认中枢
        :return:
        """
        self.__confirm = True

    def is_valid_center(self):
        """
       是否是有效的中枢
       """
        if len(self.list_bi) < 4:
            print(self.list_bi)
            return False

        return self.zg > self.zd
