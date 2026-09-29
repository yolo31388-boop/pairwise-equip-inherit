"""装备传承与继承系统

传承是"转移"而非"复制"：传承后源装备的强化等级清零，源装备进入
不可传承状态；目标装备获得源装备的强化等级，其原有强化等级按比例
转化为材料返还。传承受装备槽位类型、品质和等级差限制，材料消耗随
源装备强化等级和目标装备等级递增。
"""
from dataclasses import dataclass

# 目标装备等级低于源装备超过该等级差时，不能传承
LEVEL_GAP_LIMIT = 20


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
        # 已被消耗（完成过传承）的源装备 eid 集合
        self.inherited_items: set = set()

    def _is_consumed(self, source: Equipment) -> bool:
        return source.eid in self.inherited_items

    def _validate(self, source: Equipment, target: Equipment) -> tuple[bool, str]:
        if self._is_consumed(source):
            return False, "source equipment has already been consumed"
        if source.slot != target.slot:
            return False, "equipment slot type mismatch"
        if source.quality != target.quality:
            return False, "equipment quality mismatch"
        if source.level - target.level > LEVEL_GAP_LIMIT:
            return False, "target level too low, upgrade target first"
        return True, "ok"

    def can_inherit(self, source: Equipment, target: Equipment) -> bool:
        # 检查槽位类型、品质、源装备消耗状态和等级差限制
        return self._validate(source, target)[0]

    def get_material_cost(self, source: Equipment, target: Equipment) -> int:
        # 材料消耗随源装备强化等级和目标装备等级递增
        return 10 + source.enhance_level * 5 + target.level // 10

    def refund_target_enhance(self, target: Equipment) -> int:
        # 目标原有强化等级按比例转化为材料返还
        return target.enhance_level * 5 + target.level // 10

    def inherit(self, source: Equipment, target: Equipment) -> tuple[bool, str]:
        ok, reason = self._validate(source, target)
        if not ok:
            return False, reason

        # 目标原有强化按比例返还材料，然后转移源装备的强化等级
        self.refund_target_enhance(target)
        target.enhance_level = source.enhance_level
        # 传承是转移：源装备强化等级清零，并变为不可传承状态
        source.enhance_level = 0
        self.inherited_items.add(source.eid)
        return True, "success"
