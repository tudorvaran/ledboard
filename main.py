from data_source.time_source import TimeSource
from displays.display import Display
from displays.layers.sliding_layer import SlidingLayer
from displays.layers.string_layer import StringLayer
from managers.singlescreen_manager import SingleScreenManager
from utils import hex2tuple

BOARD_SIZE = (16, 16)

TIME_LAYER = 'timelayer-hhmm'
RAIN_LAYER = 'layer-rain'
WEATHERDISPLAY = 'display-weather'
DS_TIME = 'ds-time'
TIMEDISPLAY = 'display-time'
REFRESH_RATE = 5


DROPLETS_LOCATIONS = [
    (5, 6), (2, 0), (9, 3), (15, 10), (8, 14)
]

RAIN_NUANCES = [
    hex2tuple('256d7b'),
    hex2tuple('739ba5'),
    hex2tuple('95b4bb'),
    hex2tuple('b8ccd1')
]

def main():
    rain_board = []
    for droplet in DROPLETS_LOCATIONS:
        for k in range(0, 4):
            rain_board.append(((droplet[0] + BOARD_SIZE[0] - k) % BOARD_SIZE[0], droplet[1], RAIN_NUANCES[k]))

    manager = SingleScreenManager(REFRESH_RATE, 16, 16)

    manager.add(TIME_LAYER, {
        'instance': StringLayer(BOARD_SIZE[0], BOARD_SIZE[1], (205, 127, 50))
    })
    manager.add(DS_TIME, {
        'instance': TimeSource(DS_TIME, manager),
        'repeat': 1,
        'start': True,
        'notifiable': [TIME_LAYER]
    })

    manager.add(RAIN_LAYER, {
        'instance': SlidingLayer(BOARD_SIZE[0], BOARD_SIZE[1], rain_board, (5 / REFRESH_RATE, 0))
    })

    '''
    manager.add(TIMEDISPLAY, {
        'instance': Display(BOARD_SIZE[0], BOARD_SIZE[1]),
        'layers': [TIME_LAYER]
    })
    '''

    manager.add(WEATHERDISPLAY, {
        'instance': Display(BOARD_SIZE[0], BOARD_SIZE[1]),
        'layers': [RAIN_LAYER, TIME_LAYER]
    })


    input()
    manager.loop()
    input()
    manager.stop()

if __name__ == '__main__':
    main()