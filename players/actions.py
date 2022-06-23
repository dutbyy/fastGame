# ==================== 移动到点 ====================
def move_to_point(uid, point_x, point_y, speed):
    cmd = {
        'name': 'move_to_point',
        'uid': uid,  # int
        'position': [point_x, point_y, 0],
        'speed': speed,  # 目标速度 int
    }
    return cmd

def MoveToPointTank(uid, x, y, speed):
    return move_to_point(uid, x, y, speed)
def MoveToPointWrc(uid, x, y, speed):
    return move_to_point(uid, x, y, speed)
def MoveToPointIcv(uid, x, y, speed):
    return move_to_point(uid, x, y, speed)

# ==================== 路线移动 ====================
def move_by_points(self_id, posList, speed):
    posList = [[x, y, 0]for x,y in posList]
    return {
        'name': 'move_as_line',
        'uid': self_id,  # int
        'positions': posList,
        'speed': speed,  # 目标速度 int
    }

def MoveAsLineTank(uid, pois, speed):
    return move_by_points(uid, pois, speed)

def MoveAsLineWrc(uid, pois, speed):
    return move_by_points(uid, pois, speed)

def MoveAsLineIcv(uid, pois, speed):
    return move_by_points(uid, pois, speed)

# ==================== 上车下车 ====================
def GetOffIcv(self_id):
    return {}

def GetInIcv(self_id):
    return {}

# ==================== 目标开火 ====================
def FireTargetTank(self_id, target_id, shell_type):
    return {
        'name': 'fire',
        'uid': self_id,  # int
        'tid': target_id,
        'shell_type': shell_type,
    }

def FireTargetWrc(self_id, target_id):
    return {
        'name': 'fire',
        'uid': self_id,  # int
        'tid': target_id,
        'shell_type': -1,
    }

def FireTargetIcv(self_id, target_id, shell_type):
    return {
        'name': 'fire',
        'uid': self_id,  # int
        'tid': target_id,
        'shell_type': shell_type,
    }

# ==================== 进出战壕 ====================
def DefenseIcv(self_id, zh_id):
    return {}

def DefenseTank(self_id, zh_id):
    return {}

def UnDefenseIcv(uid, x, y, course):
    return move_to_point(uid, x, y, 60)

def UnDefenseTank(uid, x, y, course):
    return move_to_point(uid, x, y, 60)

# ==================== 方向移动（无人机）===========
def MoveDirecWrj(uid, course):
    return {
        'name': 'move_by_dir',
        'uid': uid,
        'course': course,
        'speed': 100,
        'hover': 0
    }

def HoverSelf(uid, atti):
    return {
        'name': 'move_by_dir',
        'uid': uid,
        'course': -1,
        'speed': 0,
        'hover': atti*10
    }

# ==================== 单兵移动 ====================

def MoveToPointSold(uid, x, y, speed):
    return move_to_point(uid, x, y, speed)
