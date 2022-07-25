from ctypes import *
import sys
from pynput import keyboard
from map import Map
import time
import os
import json

STD_OUTPUT_HANDLE = -11
TICK_SLEEP = 10 / 60
TREE_UPDATE = 20
CLOUD_UPDATE = 100
FIRE_UPDATE = 50
MAP_W, MAP_H = 40, 20

class COORD(Structure):
    pass

COORD._fields_ = [("X", c_short), ("Y", c_short)]

def print_at(r = 0, c = 0, s = ''):
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))

    c = s.encode("cp866")
    windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)

map = Map(MAP_W, MAP_H)

MOVES_WASD = {'w': (-1, 0), 'd': (0, 1), 's': (1, 0), 'a': (0, -1), 'ц': (-1, 0), 'в': (0, 1), 'ы': (1, 0), 'ф': (0, -1)}
MOVES_ARROWS = {keyboard.Key.up: (-1, 0), keyboard.Key.right: (0, 1), keyboard.Key.down: (1, 0), keyboard.Key.left: (0, -1)}
def on_press(key):
    global tick, pause, exited, map
    if key in MOVES_ARROWS and not pause:
        dx, dy = MOVES_ARROWS[key][0], MOVES_ARROWS[key][1]
        map.helico.move(dx, dy)
    elif hasattr(key, 'char'):
        c = key.char.lower()
        if c in MOVES_WASD.keys() and not pause:
            dx, dy = MOVES_WASD[c][0], MOVES_WASD[c][1]
            map.helico.move(dx, dy)
        elif c == 'p' or c == 'з':
            if pause:
                pause = False
            else:
                pause = True
        elif c == 'i' or c == 'ш':
            exited = True
        elif c == 'f' or c == 'а':
            data = {'helicoper': map.helico.export_data(),
                    'clouds': map.clouds.export_data(),
                    'map': map.export_data(),
                    'tick': tick}
            with open('save.json', 'w') as save:
                json.dump(data, save)
        elif c == 'l' or c == 'д':
            with open('save.json', 'r') as save:
                data = json.load(save)
                tick = data['tick']
                map.import_data(data['map'])
                map.clouds.import_data(data['clouds'])
                map.helico.import_data(data['helicoper'])
                
listener = keyboard.Listener(
    on_press=on_press,
    on_release=None)
listener.start()

def game_over():
    os.system('cls')
    print('XXXXXXXXXXXXXXXXXXX')
    print('X                 X')
    print('X    GAME OVER    X')
    print('X                 X')
    print('XXXXXXXXXXXXXXXXXXX')
    sys.exit(0)

def exit_game():
    os.system('cls')
    print('XXXXXXXXXXXXXXXXXXX')
    print('X                 X')
    print('X   GAME EXITED   X')
    print('X                 X')
    print('XXXXXXXXXXXXXXXXXXX')
    sys.exit(0)

tick = 1

pause = False
exited = False

while True:
    if pause:
        continue
    if exited:
        exit_game()
    print_at()
    print('TICK', tick, 'Keys: wasd or ⬆️⬇️⬅️➡️, f - save, l - load, p -pause, i - exite')
    map.process_helicopter()
    map.helico.print_stats()
    map.pritn_map()
    tick +=1
    time.sleep(TICK_SLEEP)
    if tick % TREE_UPDATE == 0:
        map.generate_tree()
    if tick % FIRE_UPDATE == 0:
        map.update_fires()
    if tick % CLOUD_UPDATE == 0:
        map.clouds.update()
    if map.helico.lives <= 0:
        game_over()