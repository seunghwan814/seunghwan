
import json
import os

from pico2d import *

import game_framework

import hold_state

name = "HoldState"

def enter():
    global image
    image=load_image('./resource/hold.png')
def exit():
    pass

def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_h):
                game_framework.pop_state()


def update(frame_time):
    pass

def draw(frame_time):
    image.draw(400,300)
    update_canvas()