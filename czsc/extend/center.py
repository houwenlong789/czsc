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

    def is_valid_center(self):
        """
       是否是有效的中枢
       """
        if len(self.list_bi) < 4:
            print(self.list_bi)
            return False

        return self.zg > self.zd
