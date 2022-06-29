from fastGame import motion
from fastGame.motion import MotionAction
from fastGame.weapon import AttackAction
from fastGame import weapon
from fastGame.tools import gen_cmd

class Unit:
    def __init__(self):
        self.name = ""
        self.type = ""
        self.uid = -1
        self.health = 100
        self.isalive = True
        self.log = []
        self.attack_action = None
        self.motion = motion.MotionModel()
        self.motion.unit = self
        self.weapon = weapon.WeaponMgr()
        self.umgr = None

    def exec_cmd(self, cmds):
        if not self.isalive :
            return
        for cmd in [cmds]:
            action = gen_cmd(cmd)
            # print('exec cmd', action)
            if type(action) is MotionAction:
                self.motion.exec_action(action)
            elif type(action) == AttackAction:
                unit = self.umgr.get_unit(action.uid)
                target = self.umgr.get_unit(action.tid)
                if unit.uid == 3:
                    print('Unit 3 is Attacking')
                dmg, info = self.weapon.attack(action.wtype, unit, target)
                if dmg >= 0:
                    target.health -= int(dmg)
                    if target.health <= 0:
                        target.dead()
            else:
                pass

    def run_frame(self):
        self.motion.run_frame()
        self.weapon.run_frame()

    def get_issue(self):
        issue = Issue()
        return issue

    def dead(self):
        self.health = 0
        self.motion.stop()
        self.isalive = False

    def summary(self) :
        return {
            "name": self.name,
            'uid':self.uid,
            'position': self.motion.position,
            'side': self.side,
            'speed': self.motion.speed,
            'health': self.health,
            'isalive': 1 if self.isalive else 0
        }

    def log(self, info):
        self.log.append(info)

class UnitMgr:
    def __init__(self, config):
        self.config = config
        self.units = {}

    def reset(self):
        self.__load_unit()

    def __load_unit(self):
        for _, uinfo in enumerate(self.config['units']):
            uid = uinfo['uid']
            unit = Unit()
            unit.name = uinfo['name']
            unit.type = uinfo['type']
            unit.uid = uid
            unit.motion.set_position(uinfo['position'])
            if '无人机' not in unit.name:
                unit.weapon.load(uinfo['weapons'])
            #unit.weapons = uinfo['weapons']
            unit.side = uinfo['side']
            unit.umgr = self
            self.units[uid] = unit

    def get_unit(self, uid):
        return self.units[uid]

    def run_frame(self):
        for unit in self.units.values():
            unit.run_frame()

    def summary(self):
        return [
            unit.summary() for unit in self.units.values()
        ]


