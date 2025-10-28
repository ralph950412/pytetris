import copy as cp
import keyboard
import numpy as np
import os
import random
import time

# Let's use a 2-dimensional list for the board.

# TODO: In the future, the board will be 10 x 40;
# the top 20 rows will be hidden from the UI.

# Start the game
game_status = 'game_active'

# Initialize board
board = [[0 for i in range(10)] for j in range(20)]

# Tetromino (y, x)
tetrominoes = {
    'I': [[(1, 0), (1, 1), (1, 2), (1, 3)], [(0, 2), (1, 2), (2, 2), (3, 2)]],
    'L': [[(2, 0), (1, 0), (1, 1), (1, 2)]],
    'J': [[(1, 0), (1, 1), (1, 2), (2, 2)]],
    'T': [[(0, 0), (0, 1), (0, 2), (1, 1)]],
    'O': [[(-0.5, -0.5), (-0.5, 0.5), (0.5, -0.5), (0.5, 0.5)]],
    'S': [[(1, 0), (1, 1), (0, 1), (0, 2)]],
    'Z': [[(0, 0), (0, 1), (1, 1), (1, 2)]]
}

# Select a shape and orientation (0, 1, 2, 3)
# TODO: Switch to randomizing orientation with rotatepiece()
def select_tetrominoes():
    global shape
    global tetromino
    global ymin, xmin, ymax, xmax
    shape = random.choice(list(tetrominoes))
    orientation = random.choice([i for i in range(len(tetrominoes[shape]))])
    tetromino = tetrominoes[shape][orientation]
    ymin, xmin = min([i[0] for i in tetromino]), min([i[1] for i in tetromino])
    ymax, xmax = max([i[0] for i in tetromino]), max([i[1] for i in tetromino])

# Moving
boardclone = cp.deepcopy(board)

# If the displacement is not valid, correct it until it is
def fixdisplacement():
    global dy
    global dx

    for cell in tetromino:
        if xmin + dx < 0:
            dx += 1
            fixdisplacement()
        elif xmax + dx > 9:
            dx -= 1
            fixdisplacement()
        elif ymax + dy < 0:
            dy += 1
            fixdisplacement()
            gameover()
        elif ymax + dy > 19:
            while ymax + dy > 19:
                dy -= 1
            spawn_next()
        else:
            break

def updatepiece(arg: int):
    # Make sure the displacement is valid
    fixdisplacement()

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
    tetromino = tetromino_rotated
    ymin, xmin = min([i[0] for i in tetromino]), min([i[1] for i in tetromino])
    ymax, xmax = max([i[0] for i in tetromino]), max([i[1] for i in tetromino])

def updateboard():
    # Microsoft Windows compatibility
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    board = cp.deepcopy(boardclone)
    for row in board:
        print(row)
    print(f'Pivot (y, x): ({dy}, {dx})') ##DEBUG
    print(f'Tetromino (y, x): {tetromino}') ##DEBUG
    print(f'ymax + dy: {ymax + dy}') ##DEBUG
    time.sleep(0.075)

# Spawn the tetrominoes
def spawn_next():
    global dy, dx
    select_tetrominoes()
    if shape == 'O':
        dy, dx = 0.5, 4.5
    else:
        dy, dx = 0, 4
    updatepiece(1)
    updateboard()

spawn_next()

# TODO: Gravity
# Perhaps we should create a separate thread for that

# Handle Game Over
def gameover():
    global game_status
    game_status = 'game_over'

# Controls
while not game_status == 'game_over':
    # Move left
    if keyboard.is_pressed('left'):
        updatepiece(0)
        dx -= 1
        updatepiece(1)
        updateboard()
    # Move right
    if keyboard.is_pressed('right'):
        updatepiece(0)
        dx += 1
        updatepiece(1)
        updateboard()
    # Soft drop
    if keyboard.is_pressed('down'):
        if not ymax + dy >= 19:
            updatepiece(0)
        dy += 1
        updatepiece(1)
        updateboard()
     # Hard drop
    if keyboard.is_pressed('space'):
        updatepiece(0)
        dy = 19 - ymax
        updatepiece(1)
        dy += 1
        updatepiece(1)
        updateboard()
    # Clockwise rotation
    if keyboard.is_pressed('x') or keyboard.is_pressed('up'):
        updatepiece(0)
        rotatepiece('CR')
        updatepiece(1)
        updateboard()
    # Counter-clockwise rotation
    if keyboard.is_pressed('z'):
        updatepiece(0)
        rotatepiece('CCR')
        updatepiece(1)
        updateboard()
    # 180-degree rotation
    if keyboard.is_pressed('a'):
        updatepiece(0)
        rotatepiece('180R')
        updatepiece(1)
        updateboard()