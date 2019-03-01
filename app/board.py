import numpy as np

UNOCCUPIED = 0
OCCUPIED   = -1
FOOD       = -2
HEAD       = -3

STORED_BOARDS = {}

def place_coordinates(board, coords, value):
    x_coord = coords['x']
    y_coord = coords['y']
    board[y_coord, x_coord] = value
    return


def wipe_board(board):
    board[:][:] = 0


def construct_board(state):
    print('\n\n\nNew game detected. id=' + state['game']['id'] + '\n\n')

    game_id = state['game']['id']

    board_height = state['board']['height']
    board_width = state['board']['width']
    board = np.array([[UNOCCUPIED] * board_height] * board_width)

    STORED_BOARDS[game_id] = {}
    STORED_BOARDS[game_id]['board'] = board

    return


def update_board(state):
    game_id = state['game']['id']

    board = STORED_BOARDS[game_id]['board']

    board_state = state['board']
    food_coords = board_state['food']
    snakes      = board_state['snakes']
    my_body     = state['you']['body']

    wipe_board(board)

    for coord in food_coords:
        place_coordinates(board, coord, FOOD)

    for snake in snakes:
        health = snake['health']
        snake_body = snake['body']
        for coord in snake_body[1:]:
            place_coordinates(board, coord, OCCUPIED)
        head_coord = snake_body[0]
        place_coordinates(board, head_coord, health)

    for coord in my_body[1:]:
        place_coordinates(board, coord, OCCUPIED)
    my_head_coord = my_body[0]
    place_coordinates(board, my_head_coord, HEAD)

    print('Updated board state for turn ' + str(state['turn']) + ':\n\n' + str(board) + '\n\n')

    return board


def deconstruct_board(state):
    game_id = state['game']['id']
    del STORED_BOARDS[game_id]
    print('Board deleted for finished game. id=' + game_id + '\n\n')
    return
