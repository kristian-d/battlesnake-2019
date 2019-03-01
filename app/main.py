import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response
from board import construct_board, update_board, deconstruct_board
from move import calculate_move

@bottle.route('/')
def index():
    return bottle.static_file('index.html', root='../static/')


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='../static/')


@bottle.post('/ping')
def ping():
    return ping_response()


@bottle.post('/start')
def start():
    game_state = bottle.request.json
    construct_board(game_state)
    snake_colour = '#00FF00'
    return start_response(snake_colour)


@bottle.post('/move')
def move():
    game_state = bottle.request.json
    new_board = update_board(game_state)
    my_head = (game_state['you']['body'][0]['x'], game_state['you']['body'][0]['y'])
    direction = calculate_move(new_board, my_head)
    return move_response(direction)


@bottle.post('/end')
def end():
    game_state = bottle.request.json
    deconstruct_board(game_state)
    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '127.0.0.1'),
        port=os.getenv('PORT', '49121'),
        debug=os.getenv('DEBUG', True)
    )
