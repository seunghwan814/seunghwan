import random
import json
import os

from pico2d import *

import game_framework

import title_state
import main_state
name = "EndState"

def enter():
    global image

    image=load_image('./resource/gameover.png')
    if main_state.stage==3 and main_state.bossi.hp==0:
         image=load_image('./resource/gameclear.png')
    pass

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
            if (event.type, event.key)== (SDL_KEYDOWN, SDLK_ESCAPE):
              game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
              close_canvas()
              #game_framework.quit()
              game_framework.change_state(title_state)
def update(frame_time):
    pass

def draw(frame_time):
    clear_canvas()
    image.draw(400,300)
    update_canvas()
    pass