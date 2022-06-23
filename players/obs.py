from math import isnan
WEAPON_TANK = {
    "125 мм|ВОФ36": 1,
    "125 мм|ВБК16": 2,
    "125 мм|ВБМ17": 3,
    "7.62 мм|57-Н-323С (ПСС)": 7,
    "125 мм|УБК20": 8
}

WEAPON_BZC = {
    "30 мм|УОФ8": 1,
    "7.62 мм|57-Н-323С (ПСС)": 7,
    "100 мм|УБК10М-3": 8
}


class Unit:
    def __init__(self, unit, utype):
        #print(unit)
        self.uid = int(unit['ID'])
        self.side = 'red' if unit['JB'] else 'blue'
        self.type = utype
        self.name = unit['XH']
        self.speed = unit.get('SP', 10)
        self.isalive = unit.get('WH', 1)#['WH']
        self.lon = unit.get('经度', -1)
        self.lat = unit.get('维度', -1)
        self.health = 100 - unit.get('DA', 0)
        #if self.name in ['侦打无人车', 'M1A2', 'M2A3', '04A', 'T96A']:
            #print(f'{self.name}-{self.uid} health is {self.health}')

        if utype == "坦克":
            self.weapons = {}
            for j, k in unit.get("WP", {}).items():
                if j in WEAPON_TANK:
                    self.weapons[WEAPON_TANK[j]] = k
        elif utype == "步战车":
            self.weapons = {}
            for j, k in unit.get("WP", {}).items():
                if j in WEAPON_BZC:
                    self.weapons[WEAPON_BZC[j]] = k
        else:
            self.weapons = unit.get('WP', {})
        self.origin_weapons = unit.get('WP', {})
        try:
            #self.x = round(unit['X'] - 483e4, 3)
            #self.y = round(unit['Y'] - 755e4, 3)
            self.x = round(unit['X'] , 3)
            self.y = round(unit['Y'] , 3)
            self.z = round(unit['Z'], 0)
            if isnan(self.x) or isnan(self.y) or isnan(self.z):
                print(f"Error Position {utype}-{self.uid} {self.isalive} , x, y, z is {self.x} {self.y} {self.z})")
                self.x, self.y, self.z = 0,0,0
                self.isalive = 0
        #self.state = unit['ST']
        except Exception as e:
            print('----------Error init-------------')
            print(f'Exception : {e}')
            print(unit, utype)
            self.isalive = 0
            print('---------------------------------')

class Side:
    def __init__(self, info, obs):
        self.__dict__ = {"tanks": [], 'wrjs': [], 'bzc':[], 'wrc': [], 'yzc': [], 'bgc': [], 'sb': [], 'obs': obs}
        self.__dict__.update({"qb_tanks": [], 'qb_wrjs': [], 'qb_bzc':[], 'qb_wrc': [], 'qb_yzc': [], 'qb_bgc': [], 'qbs':[], 'qb_sb': []})
        self.load(info)

    def load(self, info):
        for unit in info['units']:
            if unit['XH'] in ['T96A', 'M1A2']:
                u = Unit(unit, '坦克')
                self.tanks.append(u)
            elif unit['XH'] in ['M2A3', '04A']:
                u = Unit(unit, '步战车')
                self.bzc.append(u)
            elif '无人机' in unit['XH'] :
                u = Unit(unit, '无人机')
                self.wrjs.append(u)
            elif '无人车' in unit['XH']:
                u = Unit(unit, '无人车')
                self.wrc.append(u)
            elif '运载车' in unit['XH']:
                u = Unit(unit, '运载车')
                self.yzc.append(u)
            elif '补给车' in unit['XH']:
                u = Unit(unit, '补给车')
                self.bgc.append(u)
            elif '战壕' in unit['XH']:
                pass
            elif '士兵' in unit['XH'] :
                u = Unit(unit, '士兵')
                self.sb.append(u)
            else:
                continue
            self.obs.unit_dict[u.uid] = u
        for unit in info['qb']:
            if unit['XH'] in ['T96A', 'M1A2']:
                u = Unit(unit, '坦克')
                self.qb_tanks.append(u)
            elif unit['XH'] in ['M2A3', '04A']:
                u = Unit(unit, '步战车')
                self.qb_tanks.append(u)
            elif '无人机' in unit['XH'] :
                u = Unit(unit, '无人机')
                self.qb_wrjs.append(u)
            elif '无人车' in unit['XH']:
                u = Unit(unit, '无人车')
                self.qb_wrc.append(u)
            #elif '运载车' in unit['XH']:
            #    u = Unit(unit, '运载车')
            #    self.qb_yzc.append(u)
            #elif '补给车' in unit['XH']:
            #    u = Unit(unit, '补给车')
            #    self.qb_bgc.append(u)
            elif '士兵' in unit['XH']:
                u = Unit(unit, '士兵')
                self.qb_sb.append(u)
            else:
                continue
            self.qbs.append(u)

class Observation:
    def __init__(self, state):
        self.state = state
        self.sim_time = round(state['sim_time'], 1)
        self.unit_dict = {}
        self.red = Side(state['red'], self)
        self.blue = Side(state['blue'], self)

    def print_state_new(self):
        print("SimTime: ", self.state['sim_time'])
        units = list(self.unit_dict.values())
        units.sort(key=lambda x:int(x.uid))
        #for side in ['red', 'blue']:
        for side in ['red']:
            #print(f'{side} Observation: \nunits:')
            for unit in units:
                if unit.type not in ["坦克", "步战车", "无人车"]:
                    continue
                if unit.side == side:
                    #print(unit.__dict__)
                    print(f'''
                        \t
                        {unit.side}\t
                        {unit.type}\t
                        {unit.uid}\t
                        [{unit.x}, {unit.y}, {unit.z}]\t
                        {"alive" if unit.isalive else "dead "}\t
                        {unit.health}\t
                        {sorted(zip(unit.weapons.keys(), unit.weapons.values()))}
                        '''.replace(" ", "").replace("\n", ""))
            print('----'*20)

    def print_state_idx(self, idx):
        unit = self.unit_dict[idx]
        print(f"\t{unit.side}\t{unit.name}\t{unit.uid}\t\t {unit.x}, {unit.y}, {unit.z}, \t ---{unit.isalive} --{unit.health} --{unit.speed}")

