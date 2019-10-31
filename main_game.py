from pico2d import *
import random
import time

# Game object class here

def handle_events():
    global is_game_loop
    global player
    player_speed = 10
    events = get_events()
    for event in events:
        #Player key input
            #Arrow
        if event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            player.speed_x -= player_speed
        elif event.type == SDL_KEYUP and event.key == SDLK_LEFT:
            player.speed_x += player_speed
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            player.speed_y -= player_speed
        elif event.type == SDL_KEYUP and event.key == SDLK_DOWN:
            player.speed_y += player_speed
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            player.speed_y += player_speed
        elif event.type == SDL_KEYUP and event.key == SDLK_UP:
            player.speed_y -= player_speed
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            player.speed_x += player_speed
        elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            player.speed_x -= player_speed

        #Attack
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            player.attack = True
        elif event.type == SDL_KEYUP and event.key == SDLK_a:
            player.attack = False

        elif event.type == SDL_QUIT:
            is_game_loop = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            is_game_loop = False

#Objects

class BackGround:
    def __init__(self):
        self.image = load_image('background.png')
    def draw(self):
        self.image.draw(400,500)

class Explsion:
    def __init__(self,x,y):
        self.image = load_image('explosion.png')
        self.x, self.y = x,y
        self.life_time = 20
    def update(self):#True -> list Delete, False -> not Act
        self.life_time -= 1
        if self.life_time <= 0:
            return True
        else:
            return False
    def draw(self):
        self.image.clip_draw(0, 0, 50, 50, self.x, self.y)

class Player:
    global player_bullets

    def __init__(self):
        self.x, self.y = 240, 100
        self.speed_x = 0
        self.speed_y = 0
        self.size = 20
        #attack
        self.attack = False
        self.attack_time = 3
        #image
        self.image = load_image('fighter.png')

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.attack:
            self.attack_time -= 1
            if self.attack_time <= 0:
                player_bullets.append(Player_Bullet(self.x,self.y+20))
                self.attack_time = 3

    def draw(self):
        self.image.clip_draw(0, 0, 40, 42, self.x, self.y)

class Player_Bullet:

    def __init__(self,x,y):
        self.x, self.y = x, y
        self.speed_y = 13
        self.size = 5
        self.image = load_image('missile.png')

    def update(self):
        self.y += self.speed_y

    def draw(self):
        self.image.clip_draw(0, 0, 10, 23, self.x, self.y)

class Enemy:
    global enemy_bullets
    def __init__(self):
        self.x, self.y = random.randint(50,430),1100
        self.speed_x = 0
        self.speed_y = -5
        self.hp = 2
        self.size = 20
        self.fire_time = 50
        self.image = load_image('Enemy.png')

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        self.fire_time -= 1
        if self.fire_time <= 0:
            self.fire_time = 50
            enemy_bullets.append(Enemy_Bullet(self.x,self.y-20))

        if self.hp <= 0:
            return False

        return True

    def draw(self):
        self.image.clip_draw(0, 0, 40, 42, self.x, self.y)

class Enemy_Bullet:
    def __init__(self,x,y):
        self.x, self.y = x, y
        self.speed_y = -13
        self.size = 5
        self.image = load_image('missile_rot.png')

    def update(self):
        self.y += self.speed_y

    def draw(self):
        self.image.clip_draw(0, 0, 10, 23, self.x, self.y)

class Meteor:
    def __init__(self):
        self.x, self.y = random.randint(50,430), 700
        self.speed_x = 0
        self.speed_y = -10
        self.size = 35
        self.image = load_image('Rock.png')

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self):
        self.image.clip_draw(0, 0, 75, 37, self.x, self.y)

#Logic function
def AABB(x1,y1,size1,x2,y2,size2):
    if x1-size1 > x2+size2:
        return False
    if x1+size1 < x2-size2:
        return False
    if y1-size1 > y2+size2:
        return False
    if y1+size1 < y2-size2:
        return False
    else:
        return True

spawn_position_x = 50
spawn_dist = 50
def spawn_Enemy():
    global enemys
    global spawn_time
    global spawn_position_x
    global spawn_dist

    if spawn_position_x > 750:
        spawn_dist = -50
    elif spawn_position_x < 50:
        spawn_dist = 50

    spawn_time -= 1
    if spawn_time == 0:
        spawn_time = 10
        enemys.append(Enemy())
        enemys[-1].x = spawn_position_x
        spawn_position_x += spawn_dist


# initialization code
open_canvas(800,1000)
background = BackGround()

player = Player()
meteor = Meteor()

enemys = list()

player_bullets = list()
enemy_bullets = list()

explosion = list()

spawn_time = 100


is_game_loop = True

# game main loop code
while is_game_loop:
    handle_events()
    clear_canvas()

    spawn_Enemy()

    #Update--------------------------------------
    #meteor.update()
    player.update()

    for enemy in enemys:
        if enemy.update() == False: #hp < 0 -> list remove
            enemys.remove(enemy)

    for e_bullet in enemy_bullets:
        e_bullet.update()

    for p_bullet in player_bullets:
        p_bullet.update()

    for explo in explosion:
        if explo.update():
            explosion.remove(explo)
    # Update--------------------------------------

    #Collsion Detect------------------------------
    for bullet in enemy_bullets:
        if AABB(player.x,player.y,player.size,bullet.x,bullet.y,bullet.size):
            explosion.append(Explsion(bullet.x,bullet.y))
            enemy_bullets.remove(bullet)
    for enemy in enemys:
        for bullet in player_bullets:
            if AABB(enemy.x, enemy.y, enemy.size, bullet.x, bullet.y, bullet.size):
                explosion.append(Explsion(bullet.x, bullet.y))
                enemy.hp -= 1
                player_bullets.remove(bullet)
    # Collsion Detect------------------------------


    #Draw------------------------------------------
    background.draw()
    player.draw()

    for enemy in enemys:
        enemy.draw()
    for e_bullet in enemy_bullets:
        e_bullet.draw()
    for p_bullet in player_bullets:
        p_bullet.draw()
    for explo in explosion:
        explo.draw()
    #meteor.draw()

    update_canvas()
    # Draw------------------------------------------


    delay(0.03)

close_canvas()

# finalization code