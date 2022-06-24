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
from tools import distance_unit
import random

class AttackAction:
    def __init__(self):
        self.weapon_type = ''
        self.uid = -1
        self.tid = -1

class WeaponMgr:
    def __init__(self):
        self.weapons = {}
        self.ready = 0

    def load(self, weapons):
        for wtype, winfo in weapons.items():
            weapon = Weapon()
            weapon.weapon_type = int(wtype)
            weapon.weapon_damege = 80
            weapon.weapon_cool_done = 10
            weapon.weapon_nums = 1000
            weapon.weapon_max_nums = 1000
            self.weapons[int(wtype)] = weapon

    def attack(self, wtype, unit, tunit):
        if self.ready >0:
            return "Weapon Not Ready"
        weapon = self.weapons[wtype]
        valid_damage, status = weapon.fire(unit, tunit)
        return valid_damage, status


    def run_frame(self):
        if self.ready > 0:
            self.ready -= 1

class Weapon:
    def __init__(self):
        self.attack_distance = 1000
        self.weapon_type = 0
        self.weapon_damage = 80
        self.weapon_cool_done = 10
        self.weapon_nums = 1000
        self.weapon_max_nums = 1000

    def fire(self, unit, tunit):
        def get_base_damage(t1, t2):
            dmg = { '坦克': 150, '步战车': 120, '无人车': 120, '士兵': 60}
            defence = { '坦克': 100, '步战车': 80, '无人车':  100, '士兵':  30, '无人机': 100}
            attack = dmg[t1]
            defense = defence[t2]
            if t1 == '士兵':
                attack = attack * (2 if random.random() > 0.9 else 1)
            return attack - defense

        distance = distance_unit(unit, tunit)
        if tunit.health <=0 :
            return -1, 'Target is Dead!'
        if distance > self.attack_distance:
            return -1, f'Out Of AttackRange! {self.weapon_type}: [self.attack_distance]'
        if self.weapon_nums <= 0:
            return -1, f'Unavailable Weapon! {self.weapon_type}'
        self.weapon_nums -= 1
        base_damage = get_base_damage(unit.type, tunit.type)
        damage = base_damage * min(1, self.attack_distance/(distance+1)) * (1 if random.random()>0.3 else 0) * random.randint(5, 15) / 10
        return damage, 'Fire Success'




