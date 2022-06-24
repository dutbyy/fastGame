from motion import MotionAction
import math
def gen_cmd(cmd):
    if cmd['name'] == 'move_to_point':
        action = MotionAction()
        action.name = MotionAction.MotionType.MoveToPoint
        action.speed = cmd.get('speed', 60)
        action.positions = [cmd['position']]
    elif cmd['name'] == 'move_as_line':
        action = MotionAction()
        action.name = MotionAction.MotionType.MoveAsLine
        action.speed = cmd.get('speed', 60)
        action.positions = cmd['positions']
    elif cmd['name'] == 'move_by_dir':
        action = MotionAction()
        action.name = MotionAction.MotionType.MoveForAngle
        action.angle = cmd.get('course', -1) / 360 * 2 * math.pi
        action.hover = cmd['hover']
        action.speed = cmd['speed']
    elif cmd['name'] == 'fire':
        from weapon import AttackAction
        action = AttackAction()
        action.uid = cmd['uid']
        action.tid = cmd['tid']
        action.wtype = 1 if cmd['shell_type'] < 0 else 2
    else:
        return None
    return action

def distance_unit(unit, tunit):
    distance =  (
        (unit.motion.position[0] - tunit.motion.position[0]) ** 2 +
        (unit.motion.position[1] - tunit.motion.position[1]) ** 2 +
        (unit.motion.position[2] - tunit.motion.position[2]) ** 2
    ) ** .5
    return distance
