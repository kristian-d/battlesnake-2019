import numpy as np

UNOCCUPIED = 0
OCCUPIED = -1
FOOD = -2
HEAD = -3
TAIL = -4

STORED_BOARDS = {}


def place_coordinates(board, coords, value):
    x_coord = coords['x']
    y_coord = coords['y']
    board[y_coord, x_coord] = value
    return


def update_board(state):
    board = np.array([[UNOCCUPIED] * state['board']['height']] * state['board']['width'])

    board_state = state['board']
    food_coords = board_state['food']
    snakes = board_state['snakes']
    my_body = state['you']['body']

    for coord in food_coords:
        place_coordinates(board, coord, FOOD)

    for snake in snakes:
        snake_body = snake['body']
        for coord in snake_body[1:]:
            place_coordinates(board, coord, OCCUPIED)
        head_coord = snake_body[0]
        place_coordinates(board, head_coord, len(snake_body))

    for coord in my_body[1:]:
        place_coordinates(board, coord, OCCUPIED)
    my_head_coord = my_body[0]
    place_coordinates(board, my_head_coord, HEAD)

    # print('Updated board state for turn ' + str(state['turn']) + ':\n\n' + str(board) + '\n\n')

    return board
