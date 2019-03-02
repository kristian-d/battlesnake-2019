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


get_direction_map = {
    'up': up,
    'down': down,
    'left': left,
    'right': right,
}


def surrounding_head_weight(board, coords, size):
    challengers = 0
    for direction in DIRECTIONS:
        if size <= get_value(board, get_direction_map[direction](coords)):
            challengers = challengers + 1
    return challengers if challengers == 0 else 0.9 / challengers


def get_move_safety(board, coords, size):
    value = get_value(board, coords)
    if value not in SAFE:
        return 0

    challenger_weight = surrounding_head_weight(board, coords, size)
    return challenger_weight if challenger_weight > 0 else 1


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


def weighted_bfs(board, pos, health):
    q = [pos]
    layer_size_arr = [1, 0]
    depth = 0
    counter = 0

    food_distance = []

    space_weight = 0
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

        space_weight = space_weight + (1.0 / (depth + 1.0))

        layer_size_arr[depth + 1] = layer_size_arr[depth + 1] + len(move_coords)
        counter = counter + 1
        if counter == layer_size_arr[depth]:
            depth = depth + 1
            layer_size_arr.append(0)
            counter = 0

    food_weight = np.sum([1.0 / (np.exp(distance)) for distance in food_distance])

    available_food = len(food_distance)
    return (0.03 * health * space_weight) + ((100.0 / (health + 1)) * food_weight),\
        available_food


def get_weight(board, direction, current_head, tail, health, size):
    move_safety = get_move_safety(board, get_direction_map[direction](current_head), size)
    if move_safety < 1:
        return move_safety

    working_board = np.copy(board)
    potential_head = get_direction_map[direction](current_head)

    is_food = get_value(board, potential_head)
    if not is_food:
        working_board[tail[1], tail[0]] = UNOCCUPIED
    working_board[potential_head[1], potential_head[0]] = OCCUPIED
    (move_weight, available_food) = weighted_bfs(working_board, potential_head, health)
    move_weight = move_weight + ((8 / (available_food + 1)) * (80.0 / (health + 1))) if is_food else move_weight
    return move_weight


def possible_moves(board, coords):
    return [direction for direction in DIRECTIONS if get_value(board, get_direction_map[direction](coords)) in SAFE]


def calculate_move(board, my_head, my_tail, health, size):
    move_weights = [get_weight(board, direction, my_head, my_tail, health, size) for direction in DIRECTIONS]
    max_weight_index = 0
    for n in range(len(move_weights)):
        if move_weights[max_weight_index] < move_weights[n]:
            max_weight_index = n

    print('WEIGHTS: ' + str(move_weights))
    return DIRECTIONS[max_weight_index]
