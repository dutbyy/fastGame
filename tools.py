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
    else:
        return None
    return action
