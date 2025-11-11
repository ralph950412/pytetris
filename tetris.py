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

# If the displacement is not valid, correct it until it is
# TODO: Handle tetromino stacking.
# The idea is to refactor fixdisplacement() to detect the total '1's on the board.
# If the number changes after a movement, fix the displacement or spawn the next tetromino.
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
        elif ymax + dy < 20:
            dy += 1
            fixdisplacement()
        elif ymax + dy > 39:
            while ymax + dy > 39:
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
        if not ymax + dy >= 39:
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