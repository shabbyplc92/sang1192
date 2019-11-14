from pico2d import *
import game_framework

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 30)
        self.image.draw(1200, 30)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return 0, 0, 1600 - 1, 50

class Brick:
    def __init__(self):
        self.image = load_image('brick180x40.png')
        self.x, self.y = 400,250
        self.brick_speed = 300

    def get_speed(self):
        return self.x

    def get_y(self):
        return self.y

    def get_bb(self):
        return self.x - 90, self.y - 20, self.x + 90, self.y + 20

    def update(self):
        self.x += self.brick_speed * game_framework.frame_time
        if self.x > 1510:
            self.brick_speed = -100
        elif self.x < 100:
            self.brick_speed = 100

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())
