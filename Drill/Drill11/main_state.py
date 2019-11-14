import random
import json
import os

from pico2d import *
import game_framework
import game_world

from boy import Boy
from grass import Grass, Brick
from ball import Ball, BigBall

name = "MainState"

boy = None
grass = None
brick = None
balls = []
big_balls = []


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def collide_top(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    left_a += 20
    right_a -= 20
    top_b += 20
    bottom_b += 20

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def collide_side(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False

    return True

def enter():
    global boy
    boy = Boy()
    game_world.add_object(boy, 1)

    global grass
    grass = Grass()
    game_world.add_object(grass, 0)

    global brick
    brick = Brick()
    game_world.add_object(brick, 0)

    global balls
    balls = [Ball() for i in range(10)] + [BigBall() for i in range(10)]
    game_world.add_objects(balls, 1)


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()

    for ball in balls:
        if collide(boy, ball):
            balls.remove(ball)
            game_world.remove_object(ball)

    for ball in balls:
        if collide_top(brick, ball):
            ball.stop()
            speed = int(brick.get_speed())
            brick_y = int(brick.get_y())
            ball.stop_on_brick(speed, brick_y)

    for ball in balls:
        if collide(grass, ball):
            ball.stop()

    if collide(brick, boy):
        if boy.jumpspeed < 0:
            boy.cur_state.exit(boy)
            boy.y = 325
            if boy.distance == None:
                boy.distance = boy.x-brick.x


    if boy.y >= 320:
        if boy.jumpspeed == 0:
            if collide_side(brick,boy) == False:
                boy.cur_state.fall(boy)
                boy.distance = None


    if collide(grass, boy):
        if boy.jumpspeed != 0:
            boy.cur_state.exit(boy)
            boy.y = 101

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()






