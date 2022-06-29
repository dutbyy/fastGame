import time
import json
from fastGame.controller import Controller

class FastGame:
    def __init__(self, config):
        print('Constructing FastGame')
        self._construct(config)

    def _construct(self, config):
        self.controller = Controller(config)

    def reset(self):
        self.controller.reset()

    def step(self, commands):
        self.controller.step(commands)

    def obs(self):
        game_over = False
        if self.controller.frame > 30*60*60:
            game_over = True
        elif len([1 for unit in self.controller.unit_mgr.units.values() if unit.side == 'blue' and unit.isalive]) <= 0:
            game_over = True
        elif len([1 for unit in self.controller.unit_mgr.units.values() if unit.side == 'red' and unit.isalive]) <= 18:
            game_over = True
        if game_over :
            print('Game Over!')
        return self.controller.obs(), game_over

    def inference(self, sim_time):
        self.controller.run_frame(sim_time)
