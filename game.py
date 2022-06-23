import time
import json
from controller import Controller

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
        return self.controller.obs(), self.controller.frame > 30*60*20

    def inference(self, sim_time):
        self.controller.run_frame(30)
