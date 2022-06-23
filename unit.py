import motion
from motion import MotionAction
import weapon
from tools import gen_cmd

class Unit:
    def __init__(self):
        self.name = ""
        self.type = ""
        self.uid = -1
        self.health = 100
        self.status = 0
        self.log = []
        self.attack_action = None
        self.motion = motion.MotionModel()
        self.motion.unit = self
        self.weapons = {}

    def exec_cmd(self, cmds):
        for cmd in [cmds]:
            action = gen_cmd(cmd)
            # print('exec cmd', action)
            if type(action) is MotionAction:
                self.motion.exec_action(action)
            else : #elif type(action) == AttackAction:
                self.attack_action = action

    def run_frame(self):
        self.motion.run_frame()

    def get_issue(self):
        issue = Issue()
        return issue

    def summary(self) :
        return {
            "name": self.name,
            'uid':self.uid,
            'position': self.motion.position,
            'side': self.side,
            'speed': self.motion.speed,
            'health': self.health
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
            unit.uid = uid
            unit.motion.set_position(uinfo['position'])
            unit.weapons = uinfo['weapons']
            unit.side = uinfo['side']
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


