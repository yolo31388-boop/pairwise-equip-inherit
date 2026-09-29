"""装备传承与继承系统"""
from dataclasses import dataclass

MAX_LEVEL_GAP = 20  # 传承允许的最大等级差
REFUND_RATIO = 0.5  # 目标装备原有强化转化为材料的返还比例

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
        if source.eid in self.inherited_items:
            return False, "源装备已被传承消耗，无法再次传承"
        if source.slot != target.slot:
            return False, "装备槽位类型不匹配，无法传承"
        if source.quality != target.quality:
            return False, "装备品质不匹配，无法传承"
        if not self.can_inherit(source, target):
            return False, "等级差超过上限，请先升级目标装备"
        # 转移而非复制：目标获得源的强化等级，源强化清零并被消耗
        target.enhance_level = source.enhance_level
        source.enhance_level = 0
        self.inherited_items.add(source.eid)
        return True, "success"

    def get_material_cost(self, source: Equipment, target: Equipment) -> int:
        # 材料消耗随源装备强化等级和目标装备等级递增
        return 10 + source.enhance_level * 5 + target.level // 10

    def refund_target_enhance(self, target: Equipment) -> int:
        # 目标装备原有强化按比例转化为材料返还
        return int(target.enhance_level * 10 * REFUND_RATIO)

    def can_inherit(self, source: Equipment, target: Equipment) -> bool:
        return abs(source.level - target.level) <= MAX_LEVEL_GAP
