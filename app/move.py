import numpy as np

DIRECTIONS = ('up', 'down', 'left', 'right')

UNOCCUPIED = 0
OCCUPIED = -1
FOOD = -2
HEAD = -3
TAIL = -4
SAFE = (UNOCCUPIED, FOOD, TAIL)


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
        if np.logical_and(coord[1] < board_dimensions[0], coord[1] >= 0)\
        and np.logical_and(coord[0] < board_dimensions[1], coord[0] >= 0)\
        else OCCUPIED


def set_value(board, coord, value):
    board[coord[1], coord[0]] = value
    return


def remove_tail():
    return


def weighted_bfs(board, pos, health):
    q = [pos]
    layer_size_arr = [1, 0]
    depth = 0
    counter = 0

    food_distance = []

    weight = 0
    while q:
        current = q.pop(0)
        moves = possible_moves(board, current)
        move_coords = [get_direction_map[move](current) for move in moves]
        q.extend(move_coords)
        for coord in move_coords:
            value = get_value(board, coord)
            if value == FOOD and depth <= health:
                food_distance.append(depth)
            set_value(board, coord, OCCUPIED)

        # weight = weight + (1.0 / (2.0 * (depth + 1.0)))  # (1 / (np.exp(np.log10(depth))))
        # weight = weight + (1.0 / ((0.10 * health) - 3)) if value == FOOD else weight
        # weight = weight + (2 / depth) * (1000 * (10 - (0.1 * health))) if value == FOOD else weight

        layer_size_arr[depth + 1] = layer_size_arr[depth + 1] + len(move_coords)
        counter = counter + 1
        if counter == layer_size_arr[depth]:
            depth = depth + 1
            layer_size_arr.append(0)
            counter = 0

    print(str(food_distance))
    food_weight = np.sum([1.0 / (np.log(distance) + 1.0) for distance in food_distance])

    return food_weight


def get_weight(board, move, current_head, health):
    working_board = np.copy(board)
    new_head = get_direction_map[move](current_head)

    is_food = get_value(board, new_head)
    working_board[new_head[1], new_head[0]] = HEAD
    weight = weighted_bfs(working_board, new_head, health)
    weight = weight + (100.0 / health) if is_food else weight
    return weight


get_direction_map = {
    'up': up,
    'down': down,
    'left': left,
    'right': right,
}


def possible_moves(board, coords):
    return [direction for direction in DIRECTIONS if get_value(board, get_direction_map[direction](coords)) in SAFE]


def calculate_move(board, my_head, health):
    moves = possible_moves(board, my_head)

    num_possible_moves = len(moves)
    if num_possible_moves < 2:
        return moves[0] if num_possible_moves == 1 else 'up'

    weights = [get_weight(board, move, my_head, health) for move in moves]
    print('WEIGHTS: ' + str(weights))
    max_weight_index = 0
    for n in range(len(weights)):
        if weights[max_weight_index] < weights[n]:
            max_weight_index = n

    return moves[max_weight_index]
