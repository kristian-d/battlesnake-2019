import json
from bottle import HTTPResponse


def ping_response():
    return HTTPResponse(
        status=200
    )


def start_response(color, head, tail):
    assert type(color) is str, \
        "Color value must be string"

    return HTTPResponse(
        status=200,
        headers={
            "Content-Type": "application/json"
        },
        body=json.dumps({
            "color": "#9400D3",
            "headType": "fang",
            "tailType": "hook"
        })
    )


def move_response(move):
    assert move in ['up', 'down', 'left', 'right'], \
        "Move must be one of [up, down, left, right]"

    return HTTPResponse(
        status=200,
        headers={
            "Content-Type": "application/json"
        },
        body=json.dumps({
            "move": move
        })
    )


def end_response():
    return HTTPResponse(
        status=200
    )
