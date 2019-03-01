import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

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

    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    game_state = bottle.request.json

    return move_response(direction)


@bottle.post('/end')
def end():
    game_state = bottle.request.json

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
