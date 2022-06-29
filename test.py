from game import FastGame
from config import config
from player import Player


def init_render():

    from pyshow import RenderApi
    config = {
       "range_x": [4000, 10000],
       "range_y": [1000, 5000],
       "display_size": [1500, 1000],
       "tcolor": (0,0,0),
    }
    render = RenderApi(config)
    render.init()
    return render

def Prender(render, obs):
    #print(obs)
    icon = {
        'T96A': 'tank', '04A': 'car', 'M1A2': 'tank', 'M2A3': 'car',
        '无人机': 'uav', '步战车':'car', '坦克': 'tank', '侦打无人车':'car',
        '运载车': 'car', '补给车': 'car', '红方无人机': 'uav', '蓝方无人机': 'uav',
        '红方士兵': 'sold', '蓝方士兵': 'sold'
    }
    data = [
        {
            'name':f'{unit["name"]}-{unit["uid"]}-',
            'uid': unit['health'],
            'icon': icon[unit["name"]],
            'position':[unit['position'][1], unit['position'][0]],
            'side': unit['side'],
            'iconsize': 24,
            'textsize': 9
        }
        for unit in obs['units'] if '红方士兵' not in unit['name'] and unit['isalive']
    ]
    xdata = [
        {
            "name": "",
            'icon': 'dead',
            'position':[unit['position'][1], unit['position'][0]],
            'side': unit['side'],
            'iconsize': 24,
        }
        for unit in obs['units'] if '红方士兵' not in unit['name'] and not unit['isalive']
    ]
    #render.update({"units": data+xdata})
    render.update({"units": data})

def main():
    player = Player()
    game = FastGame(config)
    render = init_render()
    while True:
        print('start a new game')
        game.reset()
        player.reset()
        obs, done = game.obs()
        while True :
            for i in range(30):
                game.inference(10)
                commands = player.make_cmd(obs)
                game.step(commands)
                obs, done = game.obs()
                Prender(render, obs)
                if done:
                    break
            if done:
                break



if __name__ == '__main__':
    main()
