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
from fastGame.tools import distance_unit
import random

CoolDoneDict = {
    -1: 15,
    1 : 30,
    2 : 30,
    3 : 30,
    4 : 30,
    5 : 30,
    6 : 30,
    7 : 30,
    8 : 60,
}

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
            weapon.type = int(wtype)
            weapon.damege = 80
            weapon.cool_down = CoolDoneDict[weapon.type]
            weapon.cool_status = 0
            weapon.nums = 1000
            weapon.max_nums = 1000
            self.weapons[int(wtype)] = weapon

    def attack(self, wtype, unit, tunit):
        weapon = self.weapons[wtype]
        if unit.uid  == 3:
            print('tank3 attack')
            print(f'tank3 status : {weapon.cool_status}')
        if weapon.cool_status > 0:
            if unit.uid  == 3:
                print('Coll Down')
            return 0, 'Weapon Not Ready'
        valid_damage, status = weapon.fire(unit, tunit)
        weapon.cool_status = weapon.cool_down
        if unit.uid  == 3:
            print('tank3 attack')
            print(f'tank3 status : {weapon.cool_status}')
            print(self.weapons[wtype].cool_status)
        return valid_damage, status

    def run_frame(self):
        for weapon in self.weapons.values():
            if weapon.cool_status > 0:
                #print('Cool Down Wait')
                weapon.cool_status -= 1

class Weapon:
    def __init__(self):
        self.attack_distance = 1000
        self.type = 0
        self.damage = 80
        self.cool_down = 30
        self.cool_status = 0
        self.nums = 1000
        self.max_nums = 1000

    def fire(self, unit, tunit):
        def get_base_damage(t1, t2):
            dmg = { '坦克': 150, '步战车': 120, '无人车': 120, '士兵': 55}
            defence = { '坦克': 120, '步战车': 80, '无人车':  100, '士兵':  30, '无人机': 100}
            attack = dmg[t1]
            defense = defence[t2]
            if t1 == '士兵':
                attack = attack * (2 if random.random() > 0.9 else 1)
            return attack - defense

        distance = distance_unit(unit, tunit)
        if tunit.health <=0 :
            return -1, 'Target is Dead!'
        if distance > self.attack_distance:
            return -1, f'Out Of AttackRange! {self.type}: [{self.attack_distance}]'
        if self.nums <= 0:
            return -1, f'Unavailable Weapon! {self.type}'
        self.nums -= 1
        base_damage = get_base_damage(unit.type, tunit.type)
        damage = base_damage * min(1, self.attack_distance/(distance+1)) * (1 if random.random()>0.3 else 0) * random.randint(5, 15) / 10
        return damage, 'Fire Success'




