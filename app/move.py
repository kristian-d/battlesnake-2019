UNOCCUPIED = 0
OCCUPIED   = -1
FOOD       = -2

def calculate_move(board, my_head, turn):
    test = ['right', 'up', 'right', 'up', 'right', 'up', 'right', 'down', 'left', 'down', 'left', 'down']
    return test[turn]
