from players.fsm_red import FSMController as RedPlayer
from players.fsm_blue import FSMController as BluePlayer
from players.obs import Observation
import time

class Player:

    def __init__(self):
        self.obs = None
        self.env_players = [ RedPlayer(), BluePlayer() ]

    def reset(self):
        for player in self.env_players:
            player.reset()

    def make_cmd(self, obs):
        #for unit in obs['units']:
            #print(unit['position'])

        state = {
            'sim_time': 0,
            'red': {
                'units': [
                    {
                        'XH': unit['name'],
                        'ID': unit['uid'],
                        'JB': 1,
                        'SP': unit['speed'],
                        'X': unit['position'][0],
                        'Y': unit['position'][1],
                        'Z': unit['position'][2],
                        'DA': unit.get('health', 100),
                        'WH': 1,
                        'WP': {}
                    }
                    for unit in obs['units'] if unit['side'] == 'red'
                ],
                'qb': [
                    {
                        'XH': unit['name'],
                        'ID': unit['uid'],
                        'JB': 1,
                        'SP': unit['speed'],
                        'X': unit['position'][0],
                        'Y': unit['position'][1],
                        'Z': unit['position'][2],
                        'DA': unit.get('health', 100),
                        'WH': 1,
                        'WP': {}
                    }
                    for unit in obs['units'] if unit['side'] == 'blue'
                ]
            },
            'blue': {
                'units': [
                    {
                        'XH': unit['name'],
                        'ID': unit['uid'],
                        'JB': 1,
                        'SP': unit['speed'],
                        'X': unit['position'][0],
                        'Y': unit['position'][1],
                        'Z': unit['position'][2],
                        'DA': unit.get('health', 100),
                        'WH': 1,
                        'WP': {}
                    }
                    for unit in obs['units'] if unit['side'] == 'blue'
                ],
                'qb': [
                    {
                        'XH': unit['name'],
                        'ID': unit['uid'],
                        'JB': 1,
                        'SP': unit['speed'],
                        'X': unit['position'][0],
                        'Y': unit['position'][1],
                        'Z': unit['position'][2],
                        'DA': unit.get('health', 100),
                        'WH': 1,
                        'WP': {}
                    }
                    for unit in obs['units'] if unit['side'] == 'red'
                ]
            }
        }
        state = Observation(state)
        all_cmds = []
        for player in self.env_players:
            cmds = player.step(state)
            all_cmds.extend(cmds)
        #time.sleep(1)
        return all_cmds
