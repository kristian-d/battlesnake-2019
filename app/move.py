import numpy as np

DIRECTIONS = ('up', 'down', 'left', 'right')

UNOCCUPIED = 0
OCCUPIED   = -1
FOOD       = -2
TAIL       = -3
SAFE       = (UNOCCUPIED, FOOD, TAIL)

# returns the coordinate above the given coordinate
def up(coord):
    return coord[0], coord[1] - 1


# returns the coordinate below the given coordinate
def down(coord):
    return coord[0], coord[1] + 1


# returns the coordinate left of the given coordinate
def left(coord):
    return coord[0] - 1, coord[1]


# returns the coordinate right of the given coordinate
def right(coord):
    return coord[0] + 1, coord[1]


# takes a coordinate and returns the value at that coordinate on the board
def get_value(board, coord):
    board_dimensions = board.shape
    return board[coord[1], coord[0]]\
        if np.logical_and(coord[1]<board_dimensions[0], coord[1]>=0)\
            and np.logical_and(coord[0]<board_dimensions[1], coord[0]>=0)\
        else OCCUPIED


def prediction(board, move, head):
    working_board = np.copy(board)
    if not board[get_direction_map[move][head]] == FOOD:
        # remove_tail(working_board, tail)



get_direction_map = {
    'up': up,
    'down': down,
    'left': left,
    'right': right,
}
def calculate_move(board, my_head):
    possible_moves = [direction for direction in DIRECTIONS if get_value(board, get_direction_map[direction](my_head)) in SAFE]

    num_possible_moves = len(possible_moves)
    if num_possible_moves < 2:
        return possible_moves[0] if num_possible_moves == 1 else 'up'

    return np.random.choice(possible_moves)
