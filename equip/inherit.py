"""装备传承与继承系统 - 含6个bug"""
from dataclasses import dataclass

@dataclass
class Equipment:
    eid: str
    name: str
    slot: str  # weapon/armor/accessory
    level: int
    enhance_level: int = 0
    quality: str = "rare"

class InheritSystem:
    def __init__(self):
        self.inherited_items: set = set()

    def inherit(self, source: Equipment, target: Equipment) -> tuple[bool, str]:
        # bug1: 源装备不消耗
        # bug2: 不检查装备类型
        # bug4: 源装备不降等级
        target.enhance_level = source.enhance_level
        return True, "success"

    def get_material_cost(self, source: Equipment, target: Equipment) -> int:
        # bug3: 固定消耗
        return 10

    def refund_target_enhance(self, target: Equipment) -> int:
        # bug5: 目标原有强化不返还
        return 0

    def can_inherit(self, source: Equipment, target: Equipment) -> bool:
        # bug6: 无等级差限制
        return True
