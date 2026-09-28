"""装备传承与继承系统 - 红态测试"""
import pytest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from equip.inherit import InheritSystem, Equipment

class TestSourceConsumed:
    def test_source_enhance_reset(self):
        insys = InheritSystem()
        src = Equipment("s1", "old", "weapon", 100, enhance_level=15)
        dst = Equipment("d1", "new", "weapon", 100, enhance_level=0)
        insys.inherit(src, dst)
        assert src.enhance_level == 0  # bug1: 还是15
        assert dst.enhance_level == 15

class TestTypeCheck:
    def test_cannot_inherit_across_slots(self):
        insys = InheritSystem()
        src = Equipment("s1", "sword", "weapon", 100, enhance_level=10)
        dst = Equipment("d1", "ring", "accessory", 100, enhance_level=0)
        result, _ = insys.inherit(src, dst)
        assert result == False  # bug2: True

class TestCostScaling:
    def test_cost_scales_with_enhance_level(self):
        insys = InheritSystem()
        s1 = Equipment("s1", "old", "weapon", 100, enhance_level=1)
        s15 = Equipment("s15", "old", "weapon", 100, enhance_level=15)
        dst = Equipment("d1", "new", "weapon", 100)
        c1 = insys.get_material_cost(s1, dst)
        c15 = insys.get_material_cost(s15, dst)
        assert c15 > c1  # bug3: 都是10

class TestSourceNotReusable:
    def test_source_cannot_be_used_twice(self):
        insys = InheritSystem()
        src = Equipment("s1", "old", "weapon", 100, enhance_level=15)
        dst1 = Equipment("d1", "new1", "weapon", 100)
        dst2 = Equipment("d2", "new2", "weapon", 100)
        insys.inherit(src, dst1)
        result, _ = insys.inherit(src, dst2)
        assert result == False  # bug4: 源装备还能用

class TestTargetRefund:
    def test_target_existing_enhance_refunded(self):
        insys = InheritSystem()
        src = Equipment("s1", "old", "weapon", 100, enhance_level=15)
        dst = Equipment("d1", "new", "weapon", 100, enhance_level=10)
        refund = insys.refund_target_enhance(dst)
        assert refund > 0  # bug5: 0（应该返还+10的材料）

class TestLevelGapLimit:
    def test_cannot_inherit_to_much_lower_level(self):
        insys = InheritSystem()
        src = Equipment("s1", "old", "weapon", 100, enhance_level=15)
        dst = Equipment("d1", "new", "weapon", 1)  # 等级差99
        assert insys.can_inherit(src, dst) == False  # bug6: True
