import math
import random
from players.actions import *
from mylog import red_debug_print as debug_print
CONTROL_TANK = True

Uavid = list(range(13,19))
Uav_pos = [[4282, 4752], [3867, 5660], [2954, 8344], [2725, 9318], [2100, 7100], [1466, 7386]]
# 四辆坦克的序号
TankId = [1, 2, 3, 4]
Tanks_roads = [
    [[3920, 5960], [4020, 6600], [3900, 7450], [3156, 8332], [3126, 8616], [2911, 9057]],
    [[3825, 5933], [3327, 6483], [3090, 8746], [2870, 9180]],
    [[3753, 5890], [2665, 6460],               [1530, 7440]],
    [[3634, 5851], [2665, 6460],               [1512, 7560]],
]
TankRadomRoads= [
    [[2935, 8917], [3010, 8940], [3084, 9019], [2945, 9148], [2870, 9123]],
    [[2870, 9180], [2970, 9080], [2970, 9180], [2800, 9080], [2800, 9180]],
    [[1530, 7440], [1487, 7440], [1480, 7540], [1490, 7390], [1480, 7500]],
    [[1512, 7500], [1582, 7560], [1582, 7430], [1430, 7480], [1560, 7560]],
]

UgvId = [7,8,9,10,11,12]
Ugv_roads = [
    [[3330, 6264], [2887, 7442], [2152, 7903]],
    [[3330, 6264], [2887, 7442], [2222, 8034]],
    [[3330, 6264], [2887, 7442], [1793, 8063]],
    [[3330, 6264], [2887, 7442], [1528, 8140]],
    [[3330, 6264], [2887, 7442], [2283, 8477]],
    [[3330, 6264], [2887, 7442], [2276, 8395]],
]

#SVids =

IcvId = [5,6]
Icv_roads = [
    [[3402, 6333], [2858, 7429], [2309, 7808]],
    [[3402, 6333], [2900, 7520], [2212, 7690]]
]


Ugv_pos = [
    [2152, 7903],
    [2222, 8034],
    [1793, 8063],
    [1528, 8140],
    [2283, 8477],
    [2276, 8395],
]
Icv_pos = [
    [2309, 7808],
    [2212, 7690]
]
IcvLastPos =  [
    [2309, 7808],
    [2212, 7690]
]

Tank_pos = [
    [2911, 9057],
    [2870, 9180],
    [1530, 7440],
    [1512, 7560],
]

BSVID = [19, 20, 21, 22, 23, 24]
BSV_roads = [
    [[3920, 5960], [4020, 6600], [3900, 7450], [3156, 8332], [3126, 8616], [2800, 8900]],
    [[3825, 5933], [3090, 8746], [2770, 9100]],
    [[3753, 5890], [2665, 6460], [1430, 7340]],
    [[3634, 5851], [2665, 6460], [1412, 7460]],
    [[3402, 6333], [2858, 7429], [2109, 7708]],
    [[3402, 6333], [2900, 7520], [2112, 7590]]
]


UidMap = {
    'Uav': Uavid ,
    'Tan': TankId ,
    'Ugv': UgvId,
    'Icv': IcvId,
}


TankAllInPos = [
    [2235, 8618],
    [2220, 8526],
    [1629, 8317],
    [1580, 8380],
]

UgvAllInPos = [[1826, 8558], [1850, 8658], [1900, 8358], [1866, 8458], [1726, 8458], [2026, 8458]]

IcvAllInRoads = [
    [[1895, 8217], [1820, 8320], [1688, 8387]],
    [[1895, 8217], [1820, 8320], [1710, 8555]],
]


class UnitStatus:
    def __init__(self, status, idx):
        self.status = status
        self.idx = idx

# 动作执行
class ActionGenerator:
    def __init__(self):
        self.state = None
        self.action_function_map = {
            "UavDetection":             self.UavDetection,
            "UavUpping":                self.UavUp,
            "UavStop":                  self.UavStop,
            "TankGo":                   self.TankGo,
            "BSVGo":                    self.BSVGo,
            "TankSupportWaiting":       self.NoneFunc,
            "TankRandomMoving":         self.TankRandomMove,
            "UgvGo":                    self.UgvGo,
            "UgvRandomMoving":          self.UgvRandomMove,
            "IcvGo":                    self.IcvGo,
            "IcvWaiting":               self.NoneFunc,
            "IcvDown":                  self.IcvDown,
            "IcvLastMoving":            self.IcvLastMove,
            "IcvRandomMoving":          self.IcvRandomMove,
            "AutoAttackAll":            self.AutoAttackAll,
            "TankAllIn":                self.TankAllIn,
            "UgvAllIn":                 self.UgvAllIn,
            "IcvAllIn":                 self.IcvAllIn,
        }
        self.shells = {
            i: {
                1:10,
                2:10,
                3:20,
                7:2000,
                8:6
            }for i in range(1,5)
        }

    def generate(self, status_list):
        self.cmds = []
        for status in status_list:
            action_func = self.action_function_map.get(status.status, self.NoneFunc)
            action_func(status.idx)
        return [cmd for cmd in self.cmds if cmd ]

    def __calc_course(self, idx, poi):
        unit = self.state.unit_dict[idx]
        deg = math.atan2((poi[1]-unit.y), (poi[0]-unit.x)) / math.pi * 180
        return deg

    def isalive(self, uid):
        return self.state.unit_dict[uid].isalive

    def NoneFunc(self, idx):
        return

    def Distance3D(self, uid, poi):
        unit = self.state.unit_dict[uid]
        return ( (unit.x - poi[0])**2 + (unit.y - poi[1])**2 + (unit.z - poi[2])**2 )**0.5

    #-------------------------无人机动作---------------------------
    def calc_course(self, idx, poi):
        unit = self.state.unit_dict[idx]
        deg = math.atan2((poi[1]-unit.y), (poi[0]-unit.x)) / math.pi * 180
        return deg

    # 无人机探测任务
    def UavDetection(self, idx):
        uavid = Uavid[idx]
        pos = Uav_pos[idx]
        if not self.isalive(uavid):
            return
        course = self.calc_course(uavid, pos)
        if course == 0:
            course = 1
        cmd = MoveDirecWrj(uavid, course)
        self.cmds.append(cmd)
    # 无人机升空
    def UavUp(self, idx):
        uavid = Uavid[idx]
        if not self.isalive(uavid):
            return
        cmd = HoverSelf(uavid, 1)
        self.cmds.append(cmd)
    # 无人机悬停
    def UavStop(self, idx):
        uavid = Uavid[idx]
        if not self.isalive(uavid):
            return
        cmd = HoverSelf(uavid, 0)
        self.cmds.append(cmd)

    def TankGo(self, idx):
        tank_id = TankId[idx]
        pois = Tanks_roads[idx]
        if not self.isalive(tank_id):
            return
        cmd = MoveAsLineTank(tank_id, pois, 60)
        self.cmds.append(cmd)

    def TankAllIn(self, idx):
        tank_id = TankId[idx]
        poi = TankAllInPos[idx]
        if not self.isalive(tank_id):
            return
        cmd = MoveToPointTank(tank_id, poi[0], poi[1], 60)
        self.cmds.append(cmd)

    def UgvAllIn(self, idx):
        ugv_id = UgvId[idx]
        poi = UgvAllInPos[idx]
        if not self.isalive(ugv_id):
            return
        cmd = MoveToPointWrc(ugv_id, poi[0], poi[1], 90)
        self.cmds.append(cmd)

    def IcvAllIn(self, idx):
        icv_id = IcvId[idx]
        pois = IcvAllInRoads[idx]
        if not self.isalive(icv_id):
            return
        cmd = MoveAsLineIcv(icv_id, pois, 60)
        self.cmds.append(cmd)

    def BSVGo(self, idx):
        bsv_id = BSVID[idx]
        pois = BSV_roads[idx]
        if not self.isalive(bsv_id):
            return
        cmd = MoveAsLineTank(bsv_id, pois, 60)
        self.cmds.append(cmd)

    def TankRandomMove(self, idx):
        tank_id = TankId[idx]
        poi = random.choice(TankRadomRoads[idx])
        if not self.isalive(tank_id):
            return
        cmd = MoveToPointTank(tank_id, poi[0], poi[1], 20)
        self.cmds.append(cmd)

    def UgvRandomMove(self, idx):
        ugv_id = UgvId[idx]
        dx, dy = random.randint(-50, 50), random.randint(-50, 50),
        pos = Ugv_pos[idx]
        poi = [pos[0]+dx, pos[1]+dy]
        if not self.isalive(ugv_id):
            return
        cmd = MoveToPointWrc(ugv_id, poi[0], poi[1], 20)
        self.cmds.append(cmd)

    def UgvGo(self, idx):
        ugv_id = UgvId[idx]
        pois = Ugv_roads[idx]
        if not self.isalive(ugv_id):
            return
        cmd = MoveAsLineWrc(ugv_id, pois, 90)
        self.cmds.append(cmd)

    def IcvGo(self, idx):
        icv_id = IcvId[idx]
        pois = Icv_roads[idx]
        if not self.isalive(icv_id):
            return
        cmd = MoveAsLineIcv(icv_id, pois, 60)
        self.cmds.append(cmd)

    def IcvLastMove(self, idx):
        icv_id = IcvId[idx]
        poi = IcvLastPos[idx]
        if not self.isalive(icv_id):
            return
        cmd = MoveToPointIcv(icv_id, poi[0], poi[1], 60)
        self.cmds.append(cmd)

    def AutoAttackAll(self, idx):
        import json
        for unit in self.state.red.tanks:
            debug_print(f"Auto Attack Red Tanks : {unit.uid}")
            self.auto_attack(unit.uid)
        for unit in self.state.red.wrc:
            self.auto_attack(unit.uid)
        for unit in self.state.red.bzc:
            self.auto_attack(unit.uid)

    def calc_weight(self, unit, target):
        weight = -1
        dis = self.Distance3D(unit.uid, [target.x, target.y, target.z])
        if unit.type == '坦克':
            if dis < 900:
                weight = 900 - dis
                if target.type in ['坦克', '步战车']:
                    weight += 800
                elif target.type == '无人机':
                    weight += 100
                elif target.type == '士兵':
                    weight += 500
                else:
                    weight = -1
        elif unit.type == '步战车':
            if dis < 900:
                weight = 900 - dis
                if target.type in ['坦克', '步战车']:
                    weight += 500
                elif target.type == '士兵':
                    weight += 400
                else:
                    weight = -1
        elif unit.type == '无人车':
            if dis < 900:
                weight = 900 - dis
                if target.type in ['坦克', '步战车']:
                    weight += 400
                elif target.type == '士兵':
                    weight += 500
                else:
                    weight = -1
        return weight

    def auto_attack(self, uid):
        unit = self.state.unit_dict[uid]
        if not unit.isalive:
            return
        max_weight = -1
        tid = -1
        for target in self.state.red.qbs:
            if not target.isalive:
                continue
            weight = self.calc_weight(unit, target)
            if weight > max_weight:
                tid = target.uid
                max_weight = weight
        if tid > 0:
            self.attack(uid, tid)

    def attack(self, uid, tid):
        unit = self.state.unit_dict[uid]
        target = self.state.unit_dict[tid]
        cmd = None
        if unit.type == '无人车':
            shell_type = -1
            cmd = FireTargetWrc(uid, tid)
        elif unit.type == '步战车':
            if target.type in ['坦克', '步战车']:
                shell_type = random.choice([1,8])
            elif target.type == '无人机' :
                shell_type = 7
            else:
                shell_type = 1
            cmd = FireTargetIcv(uid, tid, shell_type)
        elif unit.type == '坦克':
            if target.type in ['坦克', '步战车', '士兵']:
                shells = []
                for k, v in self.shells[uid].items():
                    if v>0 and k in [1,2,3]:
                        shells.append(k)
                if not len(shells):
                    return
                shell_type = random.choice(shells)
                self.shells[uid][shell_type] -= 1
            else:
                shell_type = 7
            cmd = FireTargetTank(uid, tid, shell_type)
            debug_print(f"Tank Attack cmd : [{cmd}]")
        else:
            return
        self.cmds.append(cmd)

    def IcvDown(self, idx):
        if not self.isalive(IcvId[idx]):
            return
        return GetOffIcv(IcvId[idx])

    def IcvRandomMove(self, idx):
        icv_id = IcvId[idx]
        dx, dy = random.randint(-50, 50), random.randint(-50, 50),
        pos = Icv_pos[idx]
        poi = [pos[0]+dx, pos[1]+dy]
        if not self.isalive(icv_id):
            return
        cmd = MoveToPointIcv(icv_id, poi[0], poi[1], 20)
        self.cmds.append(cmd)



class StatusTransfer:
    def __init__(self):
        self.trans_function_map = {
            #---------------------------------------------
            "UavInit":                  self.uav_init,
            "UavUpping":                self.uav_upping,
            "UavDetection":             self.uav_detecting,
            "UavStop":                  self.uav_stoped,
            #---------------------------------------------
            "TankInit":                 self.tank_init,
            "TankGo":                   self.tank_go,
            "TankSupportWaiting":       self.tank_support_waiting,
            "TankRandomMoving":         self.tank_random_moving,
            "TankAllIn":                self.tank_all_in,
            #---------------------------------------------
            "UgvInit":                  self.ugv_init,
            "UgvGo":                    self.ugv_go,
            "UgvWaiting":               self.ugv_waiting,
            "UgvRandomMoving":          self.ugv_random_moving,
            "UgvAllIn":                 self.ugv_all_in,
            #---------------------------------------------
            "IcvInit":                  self.icv_init,
            "IcvGo":                    self.icv_go,
            "IcvWaiting":               self.icv_waiting,
            "IcvDown":                  self.icv_down,
            "IcvLastMoving":            self.icv_last_moving,
            "IcvRandomMoving":          self.icv_random_moving,
            "IcvAllIn":                 self.icv_all_in,
            #---------------------------------------------
            "BSVInit":                  self.bsv_init,
            "BSVGo":                    self.bsv_go,
            #---------------------------------------------
            "AutoAttackAll":            self.auto_attack_all,
        }
        self.reset()

    def reset(self):
        self.state = None
        self.all_in_check = True
        self.all_in_ok = False

    def transfer(self, status_list):
        if self.all_in_check:
            self.AllInCheck()
        new_status_list = []
        for status in status_list:
            if status.status[:3] in ['Ugv', 'Uav', 'Icv', 'Tan']:
                uid = UidMap[status.status[:3]][status.idx]
                if not self.state.unit_dict[uid].isalive:
                    continue
            new_status = self.trans_function_map[status.status](status.idx)
            if new_status :
                new_status_list.append(UnitStatus(new_status, status.idx))
        return new_status_list

    def AllInCheck(self):
        cnt = 0
        for unit in self.state.red.qbs:
            if not unit.isalive:
                cnt+=1
        if cnt > 10:
            self.all_in_check = False
            self.all_in_ok = True

    #----------------
    def UavHeightOK(self, idx):
        height = self.state.unit_dict[Uavid[idx]].z
        return height > 258


    def Distance2D(self, uid, poi):
        unit = self.state.unit_dict[uid]
        return ( (unit.x - poi[0])**2 + (unit.y - poi[1])**2 )**0.5

    def UavOnPlace(self, idx):
        dis =  self.Distance2D(Uavid[idx], Uav_pos[idx])
        return dis < 150

    def UgvOnPlace(self, idx):
        dis =  self.Distance2D(UgvId[idx], Ugv_pos[idx])
        return dis < 150

    def IcvOnPlace(self, idx):
        dis =  self.Distance2D(IcvId[idx], Icv_pos[idx])
        return dis < 150

    def TankOnPlace(self, idx):
        dis =  self.Distance2D(TankId[idx], Tank_pos[idx])
        return dis < 150

    def IsStoped(self, idx):
        unit = self.state.unit_dict[Uavid[idx]]
        return unit.speed < 1

    # uav-trans_function
    def uav_init(self, idx):
        if self.UavHeightOK(idx):
            return "UavDetection"
        else:
            return "UavUpping"

    def uav_upping(self, idx):
        if self.UavHeightOK(idx):
            return "UavDetection"
        else:
            return "UavUpping"

    def uav_detecting(self, idx):
        if self.UavOnPlace(idx):
            debug_print(f"无人机-{idx} is on place! Stoped!")
            return "UavStop"
        else:
            return "UavDetection"

    def uav_stoped(self, idx):
        if self.IsStoped(idx):
            return
        return "UavStop"

    def tank_init(self, idx):
        return "TankGo"

    def bsv_init(self, idx):
        return "BSVGo"

        # tank-trans_function
    def ugv_init(self, idx):
        return "UgvGo"

    def icv_init(self, idx):
        return "IcvGo"

    def auto_attack_all(self, idx):
        return "AutoAttackAll"

    def tank_go(self, idx):
        debug_print(f"Tank-{idx} Go")
        return "TankSupportWaiting"

    def bsv_go(self, idx):
        debug_print(f"BSV-{idx} Go")
        return

    def tank_support_waiting(self, idx):
        if self.TankOnPlace(idx):
            debug_print(f"Tank-{idx} is on place! Begin Random Move")
            return "TankRandomMoving"
        return "TankSupportWaiting"

    def tank_random_moving(self, idx):
        if self.all_in_ok:
            return "TankAllIn"
        return "TankRandomMoving"

    def ugv_go(self, idx):
        return "UgvWaiting"

    def ugv_waiting(self, idx):
        if self.UgvOnPlace(idx):
            debug_print(f"Ugv-{idx} is on place! Begin Random Moving")
            return "UgvRandomMoving"
        return "UgvWaiting"

    def ugv_random_moving(self, idx):
        if self.all_in_ok:
            return "UgvAllIn"
        return "UgvRandomMoving"

    def icv_go(self, idx):
        return "IcvWaiting"

    def icv_waiting(self, idx):
        if self.IcvOnPlace(idx):
            debug_print(f"Icv-{idx} is on place! Begin GetOff and Close Attack")
            #return "IcvDown"
            return "IcvLastMoving"
        return 'IcvWaiting'

    def icv_down(self, idx):
        return "IcvLastMoving"

    def icv_last_moving(self, idx):
        return "IcvRandomMoving"


    def icv_random_moving(self, idx):
        if self.all_in_ok:
            return "IcvAllIn"
        return "IcvRandomMoving"

    def tank_all_in(self, idx):
        return ''

    def icv_all_in(self, idx):
        return ''

    def ugv_all_in(self, idx):
        return ''

class FSMController:
    def __init__(self):
        self.action_executor = ActionGenerator()
        self.status_transfer = StatusTransfer()
        print("Create Red Side's Controller")

    def init_status(self):
        status = []
        [status.append(UnitStatus("UavInit", i)) for i in range(6)]
        if CONTROL_TANK:
            [status.append(UnitStatus("TankInit", i)) for i in range(4)]
            pass
        [status.append(UnitStatus("UgvInit", i)) for i in range(6)]
        [status.append(UnitStatus("IcvInit", i)) for i in range(2)]
        status.append(UnitStatus('AutoAttackAll', -1))
        self.status = status

    def reset(self):
        self.init_status()

    def step(self, state):
        self.status_transfer.state = state
        self.action_executor.state = state
        self.status = self.status_transfer.transfer(self.status)
        cmds = self.action_executor.generate(self.status)
        #print('red cmds', cmds)
        return cmds

    def pre_process(self):
        cmds = []
        with open('step_insert.ini', 'r') as f:
            data = f.readlines()
        tmp = {}
        for line in data:
            if line[:10] == '[Finished]':
                cmds.append(gen_cmd(tmp))
            elif line[:8] == '[Command':
                tmp = {}
            else:
                info = line.strip().split('=')
                if info[0] in ['name', 'action']:
                    tmp[info[0]] = info[1]
                else:
                    tmp[info[0]] = eval(info[1])
        return cmds

    def gen_cmd(infos):
        if info['name'] == '侦打无人车':
            if info['action'] == 'Move':
                cmd = MoveToPointWrc(info['uid'], info['target_x'], info['target_y'], info['speed'])
            elif info['action'] == 'Attack':
                cmd = FireTargetWrc(info['uid'], info['tid'])
        elif info['name'] == '04A':
            if info['action'] == 'Move':
                cmd = MoveToPointIcv(info['uid'], info['target_x'], info['target_y'], info['speed'])
            elif info['action'] == 'Attack':
                cmd = FireTargetIcv(info['uid'], info['tid'], info['shelltype'])
        return cmd

def main():
    print("Exec Main Function")
    import os
    import time
    from Env.client import EnvClient
    client = EnvClient(0,0,0,0)
    client.reset()
    obs = client.get_observation()
    player = FSMController()
    player.reset()
    while True:
        cmds = player.step(obs)
        print(cmds)
        client.take_action(cmds)
        time.sleep(2)
        obs = client.get_observation()
        obs.print_state()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
