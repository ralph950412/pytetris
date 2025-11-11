import copy as cp
import keyboard
import numpy as np
import os
import random
import time

# Let's use a 2-dimensional list for the board.

# TODO: Make use of pygame

# Start the game
game_status = 'game_active'

# Initialize board
board = [[0 for i in range(10)] for j in range(40)]

# Tetromino (y, x)
tetrominoes = {
    'I': [(0.5, -1.5), (0.5, -0.5), (0.5, 0.5), (0.5, 1.5)],
    'L': [(1, -1), (0, -1), (0, 0), (0, 1)],
    'J': [(0, -1), (0, 0), (0, 1), (1, 1)],
    'T': [(0, -1), (0, 0), (0, 1), (1, 0)],
    'O': [(-0.5, -0.5), (-0.5, 0.5), (0.5, -0.5), (0.5, 0.5)],
    'S': [(0, -1), (0, 0), (-1, 0), (-1, 1)],
    'Z': [(-1, -1), (-1, 0), (0, 0), (0, 1)]
}

# Select a shape and orientation
def select_tetrominoes():
    global shape
    global tetromino
    global ymin, xmin, ymax, xmax
    shape = random.choice(list(tetrominoes))
    tetromino = tetrominoes[shape]
    ymin, xmin = min([i[0] for i in tetromino]), min([i[1] for i in tetromino])
    ymax, xmax = max([i[0] for i in tetromino]), max([i[1] for i in tetromino])
    orientation = random.choice(['NONE', 'CR', 'CCR', '180R'])
    rotatepiece(orientation)

# TODO: Handle Game Over (1/2)
def gameover():
    global game_status
    game_status = 'game_over'

# Moving
boardclone = cp.deepcopy(board)

def recordtotalcells():
    cellcount = 0
    for row in boardclone:
        for cell in row:
            if cell == 1:
                cellcount += 1
    return cellcount

# If the displacement is not valid, correct it until it is
# Handle tetromino stacking
# TODO: Perhaps this could use some improvements
def fixdisplacement(arg: str):
    global dy
    global dx
    should_spawn_next = 0

    def check():
        y = int(cell[0] + dy)
        x = int(cell[1] + dx)
        if 0 <= y <= 39 and 0 <= x <= 9:
            if boardclone[y][x] == 1:
                overlapped = True
            else:
                overlapped = False
        else:
            overlapped = False
        return (y, x, overlapped)

    for cell in tetromino:
        check()
        if arg in ['right', 'auto'] and (check()[1] < 0 or check()[2]):
            dx += 1
            fixdisplacement(arg)
        elif arg in ['left', 'auto'] and (check()[1] > 9 or check()[2]):
            dx -= 1
            fixdisplacement(arg)
        elif arg in ['down', 'auto'] and (check()[0] < 0 or check()[2]):
            dy += 1
            fixdisplacement(arg)
        elif arg in ['up', 'auto'] and (check()[0] > 39 or check()[2]):
            while check()[0] > 39 or check()[2]:
                dy -= 1
            if arg == 'up':
                should_spawn_next += 1
        else:
            continue
    if should_spawn_next > 0:
        return 'spawn_next'

def updatepiece(arg: int):
    for cell in tetromino:
        y = int(cell[0] + dy)
        x = int(cell[1] + dx)
        boardclone[y][x] = arg

def rotatepiece(type):
    global tetromino
    global ymin, ymax, xmin, xmax
    # Input: rotate condition (CR, CCR, 180R)
    tetromino_rotated = []
    if type == 'CR':
        for cell in tetromino:
            y, x = cell[1], -cell[0]
            tetromino_rotated.append(tuple([y, x]))
    if type == 'CCR':
        for cell in tetromino:
            y, x = -cell[1], cell[0]
            tetromino_rotated.append(tuple([y, x]))
    if type == '180R':
        for cell in tetromino:
            y, x = -cell[0], -cell[1]
            tetromino_rotated.append(tuple([y, x]))
    if type == 'NONE':
        tetromino_rotated = tetromino
    tetromino = tetromino_rotated
    ymin, xmin = min([i[0] for i in tetromino]), min([i[1] for i in tetromino])
    ymax, xmax = max([i[0] for i in tetromino]), max([i[1] for i in tetromino])

def updateboard():
    # Microsoft Windows compatibility
    os.system('cls') if os.name == 'nt' else os.system('clear')
    board = cp.deepcopy(boardclone)
    for row in board[20:]:
        print(row)
    print(f'Pivot (y, x): ({dy}, {dx})') ##DEBUG
    print(f'Tetromino (y, x): {tetromino}') ##DEBUG
    print(f'dy: {dy}') ##DEBUG
    print(f'ymax + dy: {ymax + dy}') ##DEBUG
    print(f'ymin + dy: {ymin + dy}') ##DEBUG
    time.sleep(0.075)

# Spawn the tetrominoes
# TODO: Handle Game Over (1/2)
# End the game if the spawn gets obstructed
def spawn_next():
    global dy, dx
    select_tetrominoes()
    dy = 20 - ymin
    dx = 4.5 if shape in ['I', 'O'] else 4
    updatepiece(1)
    updateboard()

spawn_next()

# TODO: Gravity
# Perhaps we should create a separate thread for that

# Controls
while not game_status == 'game_over':
    # Move left
    if keyboard.is_pressed('left'):
        updatepiece(0)
        dx -= 1
        fixdisplacement('right')
        updatepiece(1)
        updateboard()
    # Move right
    if keyboard.is_pressed('right'):
        updatepiece(0)
        dx += 1
        fixdisplacement('left')
        updatepiece(1)
        updateboard()
    # Soft drop
    if keyboard.is_pressed('down'):
        updatepiece(0)
        dy += 1
        spawn_condition = fixdisplacement('up')
        updatepiece(1)
        updateboard()
        if spawn_condition == 'spawn_next':
            spawn_next()
    # Hard drop
    if keyboard.is_pressed('space'):
        updatepiece(0)
        dy = 39 - ymax
        fixdisplacement('up')
        updatepiece(1)
        updateboard()
        spawn_next()
    # Clockwise rotation
    if keyboard.is_pressed('x') or keyboard.is_pressed('up'):
        updatepiece(0)
        rotatepiece('CR')
        fixdisplacement('auto')
        updatepiece(1)
        updateboard()
    # Counter-clockwise rotation
    if keyboard.is_pressed('z'):
        updatepiece(0)
        rotatepiece('CCR')
        fixdisplacement('auto')
        updatepiece(1)
        updateboard()
    # 180-degree rotation
    if keyboard.is_pressed('a'):
        updatepiece(0)
        rotatepiece('180R')
        fixdisplacement('auto')
        updatepiece(1)
        updateboard()