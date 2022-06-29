from fastGame.unit import UnitMgr
from fastGame.issue import IssueMgr

class Controller:
    # 初始化单元管理和事件管理
    def __init__(self, config):
        self.config = config
        self.unit_mgr = UnitMgr(config)
        self.issue_mgr = IssueMgr(self)
        self.frame = 0

    # 重置
    def reset(self):
        self.frame = 0
        self.unit_mgr.reset()
        self.issue_mgr.reset()

    # 下发指令
    def step(self, commands):
        for cmd in commands:
            if 1:
                uid = cmd['uid']
                self.unit_mgr.get_unit(uid).exec_cmd(cmd)

    # 控制仿真向前推进一帧
    def run_frame(self, frame=1):
        for i in range(frame):
            print(self.frame)
            self.frame+=1
            self.unit_mgr.run_frame()
            self.issue_mgr.run_frame()

    def obs(self):
        return {
            "units": self.unit_mgr.summary()
        }


