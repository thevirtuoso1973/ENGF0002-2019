# Simple Pong Game.  Mark Handley, UCL, 2019

from enum import Enum

SCALE = 2
CANVAS_WIDTH = 1000//SCALE
CANVAS_HEIGHT = 700//SCALE
BAT_HEIGHT = 100//SCALE
BAT_WIDTH = 20//SCALE
BALL_SIZE = 20//SCALE
BALL_SPEED = 8//SCALE
BAT_SPEED = 10//SCALE

class Direction(Enum):
    NONE = 0
    UP = 1
    DOWN = 2

def reverse_direction(dirn):
    if dirn == Direction.UP:
        return Direction.DOWN
    elif dirn == Direction.DOWN:
        return Direction.UP
    else:
        return dirn
