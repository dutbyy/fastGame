import math
from players.actions import *
from mylog import debug_print

Uavid = [39, 40, 41]
Uav_pos = [[3000, 7000], [2000, 8000], [3000, 9000]]
# 四辆坦克的序号
TankId = [31, 32, 33, 34]
TankInitPos = [[3235.577, 7423.708], [2814.969, 7127.931], [3178.947, 7004.862], [3369.018, 7139.991]]
# 四辆坦克的最终壕沟编号
ZhId = [42, 45, 44, 43]
ZhPos = [[2068, 8641], [1936, 8560], [1831, 8487], [1676, 8298]]
# 四辆坦克撤出壕沟的位置
TankOutTrenchPos = [[3200, 7500], [2772, 7223], [3050, 7050], [3362, 7162]]
# 四辆坦克掩护/防守位置
TankTaskPos =  [[3984, 8065], [3625, 7739], [2976, 7190], [3126, 7437]]
# 四辆坦克的进壕沟位置
TankInTrenchPos =   [[2030, 8692], [1637, 8388], [1745, 8556], [1916, 8700]]

# 步兵班步兵ID
SoldLId = list(range(73, 79))
SoldRId = list(range(79, 85))
SoldId = list(range(85, 91))
#SoldId = [85, 86, 87, 88, 89, 90]
SoldPos = [[1919.15, 8525.2], [1957, 8553.6], [1975.5, 8563.5], [2012.2, 8588.5], [2047.8, 8611.5], [2069.8, 8624.5]]
SoldLeftPos = [[1654.122, 8339.503], [1644.402, 8352.105], [1631.910, 8366.206], [1603.103, 8404.024], [1583.605, 8428.501], [1576.005, 8443.106]]
SoldRightPos = [[1654.122, 8339.503], [1644.402, 8352.105], [1631.910, 8366.206], [1603.103, 8404.024], [1583.605, 8428.501], [1576.005, 8443.106]]

# 步兵进入壕沟位置

class UnitStatus:
    def __init__(self, status, idx):
        self.status = status
        self.idx = idx
#

# 动作执行
class ActionGenerator:
    def __init__(self):
        self.state = None
        self.action_function_map = {
            "":                         self.NoneFunc,
            "UavDetection":             self.UavDetection,
            "UavUpping":                self.UavUp,
            "UavStop":                  self.UavStop,
            "TankEventWaiting":         self.NoneFunc,
            "TankRetreatPreparing":     self.TankOutTrench,
            "TankTaskPreparing":        self.TankOutTrench,
            "TankCoverDoing":           self.TankTask,
            "TankTaskDoing":            self.TankTask,
            "TankRetreating":           self.TankRetreat,
            "TankInTrenchWaiting":      self.NoneFunc,
            "TankInTrench":             self.TankInTrench,
            "SoldEventWaiting":         self.NoneFunc,
            "SoldSupportMoving":        self.SoldTransport,
            "SoldSupportLeftMoving":    self.SoldTransportLeft,
            "SoldSupportRightMoving":   self.SoldTransportRight
        }

    def generate(self, status_list):
        self.cmds = []
        for status in status_list:
            action_func = self.action_function_map.get(status.status, self.NoneFunc)
            cmd = action_func(status.idx)
            if cmd:
                self.cmds.append(cmd)
        return self.cmds

    def __calc_course(self, idx, poi):
        unit = self.state.unit_dict[idx]
        deg = math.atan2((poi[1]-unit.y), (poi[0]-unit.x)) / math.pi * 180
        return deg

    def isalive(self, uid):
        return self.state.unit_dict[uid].isalive

    def NoneFunc(self, idx):
        return ''

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
            return ''
        course = self.calc_course(uavid, pos)
        if course == 0:
            course = 1
        cmd = MoveDirecWrj(uavid, course)
        return cmd

    # 无人机升空
    def UavUp(self, idx):
        uavid = Uavid[idx]
        if not self.isalive(uavid):
            return ''
        cmd = HoverSelf(uavid, 1)
        return cmd
    # 无人机悬停
    def UavStop(self, idx):
        uavid = Uavid[idx]
        if not self.isalive(uavid):
            return ''
        cmd = HoverSelf(uavid, 0)
        return cmd

    #-------------------------坦克动作---------------------------
    # 坦克撤出警戒壕沟
    def TankOutTrench(self, idx):
        # 四辆坦克撤出壕沟的位置
        tank_id = TankId[idx]
        poi = TankOutTrenchPos[idx]
        if not self.isalive(tank_id):
            return ''
        cmd = UnDefenseTank(tank_id, poi[0], poi[1], -66.3)
        return cmd#self.cmds.append(cmd)

    # tank额外任务: 1,2右侧防守，3,4掩护撤退
    def TankTask(self, idx):
        i = idx
        tank_id = TankId[idx]
        poi = TankTaskPos[idx]
        if not self.isalive(tank_id):
            return ''
        cmd = MoveToPointTank(tank_id, poi[0], poi[1], 60)
        return cmd

    # tank-撤退回主阵地准备进战壕
    def TankRetreat(self, idx):
        # 四辆坦克的进壕沟位置
        line1 = [[2350, 8250], [2130, 8394],[2060, 8500]]
        line2 = [[1895, 8217], [1820, 8320]]
        safeline = [line1, line2, line2, line1]
        tank_id = TankId[idx]
        poi = TankInTrenchPos[idx]
        if not self.isalive(tank_id):
            return ''
        pois = safeline[idx]+[TankInTrenchPos[idx]]
        if idx == 1:
            pois = [[2487, 7006], [2332, 7645], [2135, 7718]] + pois
        cmd = MoveAsLineTank(tank_id, pois, 60)
        return cmd

    # 坦克进防守壕沟
    def TankInTrench(self, idx):
        i = idx
        tank_id = TankId[idx]
        zhid = ZhId[idx]
        if not self.isalive(tank_id):
            return ''
        cmd = DefenseTank(tank_id, zhid)
        return cmd

    #---------------------------单兵转移-----------------------------
    def SoldTransport(self, idx):
        if not self.isalive(SoldId[idx]):
            return ''
        cmd = MoveToPointSold(SoldId[idx], SoldPos[idx][0], SoldPos[idx][1], 10)
        return cmd

    def SoldTransportLeft(self, idx):
        if not self.isalive(SoldId[idx]):
            return ''
        cmd = MoveToPointSold(SoldId[idx], SoldLeftPos[idx][0], SoldLeftPos[idx][1], 10)
        return cmd

    def SoldTransportRight(self, idx):
        if not self.isalive(SoldId[idx]):
            return ''
        cmd = MoveToPointSold(SoldId[idx], SoldLeftPos[idx][0], SoldLeftPos[idx][1], 10)
        return cmd

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
            "TankEventWaiting":         self.tank_event_waiting,
            "TankTaskPreparing":        self.tank_task_preparing,
            "TankTaskDoing":            self.tank_task_doing,
            "TankRetreatPreparing":     self.tank_retreat_preparing,
            "TankCoverDoing":           self.tank_cover_doing,
            "TankRetreating":           self.tank_retreating,
            "TankInTrench":             self.tank_in_trench,
            "TankInTrenchWaiting":      self.tank_in_trench_waiting,
            #---------------------------------------------
            "SoldInit":                 self.sold_init,
            "SoldEventWaiting":         self.sold_event_waiting,
            "SoldSupportMoving":        self.sold_support_moving,
            "SoldSupportLeftMoving":    self.sold_support_left_moving,
            "SoldSupportRightMoving":   self.sold_support_right_moving,
        }
        self.reset()

    def reset(self):
        self.state = None
        self.cross_river_check = True
        self.right_alert_check = True
        self.sold_support_check = True
        self.support_sold = False
        self.support_sold_left = False
        self.support_sold_right = False
        self.right_alert = False
        self.cross_river = False

    def transfer(self, status_list):
        if self.cross_river_check:
            self.CrossRiverCheck()
        if self.right_alert_check:
            self.RightAlertCheck()
        if self.sold_support_check:
            self.SoldSupportCheck()
        new_status_list = []
        for status in status_list:
            new_status = self.trans_function_map[status.status](status.idx)
            if new_status:
                new_status_list.append(UnitStatus(new_status, status.idx))
        return new_status_list

    #----------------
    def RightAlertCheck(self):
        def is_circuitous(x, y):
            return x > 4000 and y > 7000
        if len([1 for unit in self.state.blue.qbs if is_circuitous(unit.x, unit.y)]) > 0 :
            self.right_alert = True
            self.right_alert_check = False

    def CrossRiverCheck(self):
        def iscross(x, y):
            # return True
            return x+3000 > y
        cross_num = len([1 for unit in self.state.blue.qbs if unit.type != '无人机' and iscross(unit.x, unit.y)])
        if cross_num >= 2:
            self.cross_river = True
            self.cross_river_check = False
            self.right_alert_check = False

    def SoldSupportCheck(self):
        debug_print("SoldSupportCheck")
        def left_dmg(x, y):
            # return True
            return x<2000 and y >7500
        def right_dmg(x, y):
            return x<2500 and y >8500
        def sold_dmg():
            if len([ 1 for uid in SoldLId if self.state.unit_dict[uid].isalive]) <= 3:
                return True
            elif len ([ 1 for uid in SoldRId if self.state.unit_dict[uid].isalive]) <=3:
                return True
        self.sold_support_check = False
        if sold_dmg():
            self.support_sold = True
        elif len([1 for unit in self.state.blue.qbs if left_dmg(unit.x, unit.y)]) > 1:
            self.support_sold_left = True
        elif len([1 for unit in self.state.blue.qbs if right_dmg(unit.x, unit.y)]) > 1:
            self.support_sold_right = True
        else :
            self.sold_support_check = True

    #----------------
    def UavHeightOK(self, idx):
        height = self.state.unit_dict[Uavid[idx]].z
        return height > 300

    def Distance(self, uid, poi):
        unit = self.state.unit_dict[uid]
        return ((unit.x - poi[0])**2 + (unit.y - poi[1])**2)**0.5

    def UavOnPlace(self, idx):
        dis =  self.Distance(Uavid[idx], Uav_pos[idx])
        return dis < 150

    def SupportOnPlace(self, idx):
        dis =  self.Distance(SoldId[idx], SoldPos[idx])
        return dis < 1
    def SupportLeftOnPlace(self, idx):
        dis =  self.Distance(SoldId[idx], SoldLeftPos[idx])
        return dis < 1
    def SupportRightOnPlace(self, idx):
        dis =  self.Distance(SoldId[idx], SoldRightPos[idx])
        return dis < 1

    def IsStoped(self, idx):
        unit = self.state.unit_dict[Uavid[idx]]
        return unit.speed < 1

    #------------------------------
    def TankOutOfTrend(self, idx):
        dis = self.Distance(TankId[idx], TankInitPos[idx])
        return dis > 8

    def TaskDone(self, idx):
        dis = self.Distance(TankId[idx], TankTaskPos[idx])
        return dis < 50

    def PreInTrench(self, idx):
        dis = self.Distance(TankId[idx], TankInTrenchPos[idx])
        return dis < 20

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
            debug_print(f"无人机-{idx} 已就位" )
            return "UavStop"
        else:
            return "UavDetection"

    def uav_stoped(self, idx):
        if self.IsStoped(idx):
            return ""
        return "UavStop"

    # tank-trans_function
    def tank_init(self, idx):
        return "TankEventWaiting"

    def tank_event_waiting(self, idx):
        if self.cross_river:
            return "TankRetreatPreparing"
        if idx in [0,1] and self.right_alert:
            return 'TankTaskPreparing'
        return "TankEventWaiting"

    def tank_task_preparing(self, idx):
        if self.TankOutOfTrend(idx):
            debug_print(f"坦克-{idx} 已出战壕" )
            return "TankTaskDoing"
        else:
            return "TankTaskPreparing"

    def tank_task_doing(self, idx):
        if self.TaskDone(idx):
            return ""
        else:
            return "TankTaskDoing"

    def tank_retreat_preparing(self, idx):
        if self.TankOutOfTrend(idx):
            debug_print(f"坦克-{idx} 已出战壕" )
            if idx in [3, 4]:
                return "TankCoverDoing"
            else:
                return "TankRetreating"
        else:
            return "TankRetreatPreparing"

    def tank_cover_doing(self, idx):
        if self.TaskDone(idx):
            return "TankRetreating"
        else:
            return "TankCoverDoing"

    def tank_retreating(self, idx):
        return "TankInTrenchWaiting"

    def tank_in_trench_waiting(self, idx):
        if self.PreInTrench(idx):
            debug_print(f"坦克-{idx} 准备进入战壕" )
            return "TankInTrench"
        return "TankInTrenchWaiting"

    def tank_in_trench(self, idx):
        return ""

    # tank-trans_function
    def sold_init(self, idx):
        return "SoldEventWaiting"

    def sold_event_waiting(self, idx):
        if self.support_sold:
            debug_print(f"士兵-{idx} 进行前方支援" )
            return "SoldSupportMoving"
        elif self.support_sold_left:
            debug_print(f"士兵-{idx} 进行左侧支援" )
            return "SoldSupportLeftMoving"
        elif self.support_sold_right:
            debug_print(f"士兵-{idx} 进行右侧支援" )
            return "SoldSupportRightMoving"
        else:
            return "SoldEventWaiting"

    def sold_support_moving(self, idx):
        if self.SupportOnPlace(idx):
            debug_print(f"士兵-{idx} 进行支援" )
            return ""
        else:
            return "SoldSupportMoving"
    def sold_support_left_moving(self, idx):
        if self.SupportLeftOnPlace(idx):
            return ""
        else:
            return "SoldSupportLeftMoving"

    def sold_support_right_moving(self, idx):
        if self.SupportRightOnPlace(idx):
            return ""
        else:
            return SoldSupportRightMoving

class FSMController:
    def __init__(self):
        self.action_executor = ActionGenerator()
        self.status_transfer = StatusTransfer()
        print("Create Blue Side's Controller")

    def init_status(self):
        status = []
        [status.append(UnitStatus("UavInit", i)) for i in range(3)]
        [status.append(UnitStatus("TankInit", i)) for i in range(4)]
        [status.append(UnitStatus("SoldInit", i)) for i in range(6)]
        self.status = status

    def reset(self):
        self.init_status()
        #self.action_executor.reset()
        self.status_transfer.reset()

    def step(self, state):
        self.status_transfer.state = state
        self.action_executor.state = state
        self.status = self.status_transfer.transfer(self.status)
        cmds = self.action_executor.generate(self.status)
        return cmds



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
        #print(cmds)
        client.take_action(cmds)
        time.sleep(2)
        obs = client.get_observation()
        #obs.print_state()


if __name__ == '__main__':
    main()
