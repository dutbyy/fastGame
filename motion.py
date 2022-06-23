# 负责所有单位的机动行为
#   1. 支持指定点和指定路线(点列表)
#   2. 维护当前物体的运动状态
#       speed, target_position, motion_action
import math
from enum import Enum
from copy import deepcopy

def distance(a, b):
    return sum([(a[i]-b[i])**2 for i in range(2)]) ** .5


# 定义机动的动作
class MotionAction:
    class MotionType(Enum):
        MoveToPoint     = 1
        MoveAsLine      = 2
        MoveForAngle    = 3
        #MoveAsCircle    = 4
        #MoveRandom      = 5

    def __init__(self, mtype=None, position=[]):
        self.name = mtype
        self.speed = 0
        self.positions = [position, ]
        self.angle = 0.0
        self.hover = 0.0

# 通用机动模型，支持指定点移动和指定路线移动
class MotionModel:
    def __init__(self):
        self.unit = None
        self.position = [0, 0, 0]
        self.speed = 0.0
        self.target_position = None
        self.acceleration = None
        self.moving_angle = None
        self.hover = 0
        self.acceleration_angle = None
        self.motion_action = None
        self.tpf = .03#2TimePerFrame

    def set_position(self, position):
        self.position = position

    def set_speed(self, speed):
        speed = max(min(10000, speed), 0)
        self.speed = speed * 1000 / 3600

    # 执行指定动作.
    #   更新运动状态
    #   会用新的指定的动作直接覆盖之前的状态
    def exec_action(self, action):
        self.motion_action = deepcopy(action)
        self.set_speed(action.speed)
        self.__update_state()

    # 推进一帧
    # 根据状态来决定下一帧的状态
    def run_frame(self):
        if self.target_position:
            moving_distance = self.tpf * self.speed
            tdis = distance(self.position, self.target_position)
            if tdis < moving_distance:
                self.position[:2] = self.target_position[:2]
                self.target_position = None
            else:
                percent = moving_distance / tdis
                self.position = [self.position[idx] + percent * (self.target_position[idx] - self.position[idx])  for idx in range(2)] + [0]
            if not self.target_position:
                self.__update_state()
        elif self.moving_angle or self.hover:
            moving_distance = self.tpf * self.speed
            move_x = moving_distance * math.cos(self.moving_angle)
            move_y = moving_distance * math.sin(self.moving_angle)
            move_z = self.tpf * self.hover
            self.position = [self.position[0] + move_x, self.position[1] + move_y, self.position[2] + move_z]

    # 更新当前的运动状态
    #   1. 主动更新了当前的动作时
    #   2. 移动过程中，完成之前的动作了
    def __update_state(self):
        if not self.motion_action:
            return
        if self.motion_action.name == MotionAction.MotionType.MoveToPoint:
            self.target_position = self.motion_action.positions[0]
            self.motion_action = None
        elif self.motion_action.name == MotionAction.MotionType.MoveAsLine:
            #print(f'update move as line, {self.unit.name},{self.unit.uid} {self.position}, {self.motion_action.positions}, {self.speed}')
            self.target_position = self.motion_action.positions[0]
            self.motion_action.positions.pop(0)
            if len(self.motion_action.positions) <= 0:
                self.motion_action = None
        elif self.motion_action.name == MotionAction.MotionType.MoveForAngle:
            self.target_position = None
            self.moving_angle = self.motion_action.angle
            self.hover = self.motion_action.hover
            self.motion_action = None
        else:
            raise Exception("Not Support Motion Action [{self.motion_action.name}]!")
