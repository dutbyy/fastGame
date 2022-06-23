# 武器类型
# @design
#   attack_distance :（m)
#   weapon_type     : 0(火炮), 1(穿甲弹), 2(机枪), 3(导弹)
#       weapon_type 对应的会用武器攻击单位加成
#   weapon_hit_prob : 命中率公式, 应该是一个动态方法
#   weapon_damage   : 武器伤害
#   weapon_cool_done: 武器使用间隔(s)
#   weapon_nums     : 武器弹药数量
#   weapon_max_nums : 武器最大弹药数量


class Weapon:
    def __init__(self):
        self.attack_distance = 1000
        self.weapon_type = 0
        self.weapon_damege = 80
        self.weapon_cool_done = 10
        self.weapon_nums = 1000
        self.weapon_max_nums = 1000
