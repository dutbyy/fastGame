
class Issue:
    def __init__(self):
        print('create an issue')

    def update(self):
        raise NotImplementedError

class AttackIssue:
    def __init__(self, uid, tid, shell_type):
        pass

    def update(self):
        unit = getUnit(uid)
        target = getUnit(target)
        dmg = calc_dmg(unit, target, shell_type)
        target.health -= dmg

class IssueMgr:
    def __init__(self, controllor):
        self.issues = []

    def reset(self):
        self.issues = []

    def call(self):
        for issue in self.issues:
            issue.update()

    def run_frame(self):
        self.call()
