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
        self.roadImage = load_image('Road.png')
        self.backGroundImage = load_image('background.png')
        self.y = 0
        self.backGroundMusic = load_wav('music.wav')
        self.backGroundMusic.set_volume(64)
        self.backGroundMusic.repeat_play()
    def draw(self):
        self.y += 10
        self.backGroundImage.draw(300,400)

        if self.y > 3000:
            self.y -= 3000


        self.roadImage.clip_draw(0, 0 ,300 , 3000,300,400-self.y)
        self.roadImage.clip_draw(0, 0, 300, 3000, 300, 3400-self.y)

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
        self.size = 30
        self.hp = 10
        #attack
        self.attack = False
        self.attack_time = 3
        #image
        self.image = load_image('fighter.png')
        self.power = 0

        self.missileSound = load_wav('missile.wav')
        self.missileSound.set_volume(32)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.attack:
            self.attack_time -= 1
            if self.attack_time <= 0:
                if self.power == 0:
                    player_bullets.append(Player_Bullet(self.x,self.y+20))
                    self.attack_time = 3
                elif self.power == 1:
                    player_bullets.append(Player_Bullet(self.x+4,self.y+20))
                    player_bullets.append(Player_Bullet(self.x - 4, self.y + 20))
                    self.attack_time = 3
                elif self.power >= 2:
                    player_bullets.append(Player_Bullet(self.x+5,self.y+20))
                    player_bullets.append(Player_Bullet(self.x, self.y + 20))
                    player_bullets.append(Player_Bullet(self.x - 5, self.y + 20))
                    self.attack_time = 3
                self.missileSound.play()


    def power_up(self):
        self.power+=1

    def draw(self):
        self.image.clip_draw(0, 0, 80, 48, self.x, self.y,60,60)

class ItemL:
    def __init__(self,x,y):
        self.image = load_image('itemL.png')
        self.y = y
        self.x = x
        self.size = 40
    def draw(self):
        self.y -= 10
        self.image.clip_draw(0, 0 ,90 ,95,self.x,self.y)

class Player_Bullet:

    def __init__(self,x,y):
        self.x, self.y = x, y
        self.speed_y = 13
        self.size = 5
        self.image = load_image('missile.png')

    def update(self):
        self.y += self.speed_y

    def draw(self):
        self.image.clip_draw(0, 0, 10, 23, self.x, self.y,10,15)

class Enemy:
    global enemy_bullets
    def __init__(self):
        self.x, self.y = random.randint(50,430),1100
        self.speed_x = 0
        self.speed_y = -5
        self.hp = 5
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

        if self.y <= 0:
            return False

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
        self.image.clip_draw(0, 0, 10, 23, self.x, self.y,10,15)

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

class Boss:
    global enemy_bullets

    def __init__(self):
        self.x, self.y = 300, 1100
        self.speed_x = 0
        self.speed_y = -5
        self.hp = 300
        self.size = 150
        self.fire_time = 50
        self.fire_time2 = 50
        self.image = load_image('Boss.png')

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.y < 700:
            self.y = 700

        self.fire_time -= 1
        if self.fire_time <= 0:
            self.fire_time = 50
            enemy_bullets.append(Boss_Bullet(random.randint(0, 600), self.y - 20))
            enemy_bullets.append(Boss_Bullet(random.randint(0, 600), self.y - 20))
            enemy_bullets.append(Boss_Bullet(random.randint(0, 600), self.y - 20))

        self.fire_time2 -=2
        if self.fire_time2 <= 0:
            self.fire_time2 = 50
            enemy_bullets.append(Enemy_Bullet(random.randint(0, 600), self.y - 20))
            enemy_bullets.append(Enemy_Bullet(random.randint(0, 600), self.y - 20))
            enemy_bullets.append(Enemy_Bullet(random.randint(0, 600), self.y - 20))
            enemy_bullets.append(Enemy_Bullet(random.randint(0, 600), self.y - 20))
            enemy_bullets.append(Enemy_Bullet(random.randint(0, 600), self.y - 20))
            enemy_bullets.append(Enemy_Bullet(random.randint(0, 600), self.y - 20))


        if self.hp <= 0:
            return False

        return True

    def draw(self):
        self.image.clip_draw(0, 0, 410, 157, self.x, self.y)

class Boss_Bullet:
    def __init__(self,x,y):
        self.x, self.y = x, y
        self.speed_y = -13
        self.size = 15
        self.image = load_image('boss_bullet.png')

    def update(self):
        self.y += self.speed_y
        if player.x < self.x:
            self.x -= (self.x-player.x)/25
        elif player.x > self.x:
            self.x -= (self.x-player.x)/25

    def draw(self):
        self.image.clip_draw(0, 0, 30, 30, self.x, self.y)

class UI:
    def __init__(self):
        self.image = load_image('heart.png')
        self.gameOverImage = load_image('gameover.png')


    def draw(self):
        global is_game_loop
        if player.hp<= 0:
            is_game_loop = False

        for i in range(0,player.hp):
            self.image.clip_draw(0, 0, 424, 369, 20+(i*30),750,30,30)

    def gameOverDraw(self):
        self.gameOverImage.clip_draw(0,0,359,248,300,450)


class SoundManager:
    def __init__(self):
        self.missileCollisionSound = load_wav('explosion01.wav')
        self.enemyDeadSound = load_wav('explosion02.wav')
        self.bossDeadSound = load_wav('explosion04.wav')
        self.gameOverSound = load_wav('gameover.wav')

        self.missileCollisionSound.set_volume(20)
        self.enemyDeadSound.set_volume(40)
        self.bossDeadSound.set_volume(20)
        self.gameOverSound.set_volume(70)

    def playSoundBossDead(self):
        self.bossDeadSound.play()

    def playSoundMissleCollision(self):
        self.missileCollisionSound.play()

    def playSoundEnemyDead(self):
        self.enemyDeadSound.play()
    def playSoundGameOver(self):
        self.gameOverSound.play()


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

    spawn_position_x = random.randint(0,600)

    spawn_time -= 1
    if spawn_time == 0:
        spawn_time = 30
        enemys.append(Enemy())
        enemys[-1].x = spawn_position_x
        spawn_position_x += spawn_dist


# initialization code
open_canvas(600,800)
background = BackGround()

player = Player()
meteor = Meteor()
ui = UI()
soundMgr = SoundManager()
enemys = list()

item = list()

player_bullets = list()
enemy_bullets = list()

explosion = list()

spawn_time = 100
game_time = 0


is_game_loop = True
game_over = False

# game main loop code
while is_game_loop:



    handle_events()
    clear_canvas()

    if game_time < 500:
        spawn_Enemy()
    elif game_time == 500:
        enemys.append(Boss())


    #Update--------------------------------------
    #meteor.update()
    player.update()

    for enemy in enemys:
        if enemy.update() == False: #hp < 0 -> list remove
            rand = random.randint(0,10)
            if rand > 8:
                item.append(ItemL(enemy.x,enemy.y))
            soundMgr.playSoundEnemyDead()
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
            player.hp -= 1
            enemy_bullets.remove(bullet)
    for enemy in enemys:
        for bullet in player_bullets:
            if AABB(enemy.x, enemy.y, enemy.size, bullet.x, bullet.y, bullet.size):
                explosion.append(Explsion(bullet.x, bullet.y))
                enemy.hp -= 1
                player_bullets.remove(bullet)

    for it in item:
        if AABB(player.x,player.y,player.size,it.x,it.y,it.size):
            player.power_up()
            item.remove(it)
    # Collsion Detect------------------------------


    #Draw------------------------------------------
    background.draw()
    player.draw()

    for it in item:
        it.draw()

    for enemy in enemys:
        enemy.draw()
    for e_bullet in enemy_bullets:
        e_bullet.draw()
    for p_bullet in player_bullets:
        p_bullet.draw()
    for explo in explosion:
        explo.draw()
    #meteor.draw()
    ui.draw()

    update_canvas()
    # Draw------------------------------------------


    delay(0.03)
    game_time += 1


soundMgr.playSoundGameOver()

is_game_loop = True
while is_game_loop:
    handle_events()
    explosion.append(Explsion(random.randint(0,600),random.randint(0,800)))
    explosion.append(Explsion(random.randint(0, 600), random.randint(0, 800)))

    for explo in explosion:
        if explo.update():
            explosion.remove(explo)

    for explo in explosion:
        explo.draw()

    ui.gameOverDraw()
    update_canvas()
    delay(0.03)

close_canvas()

# finalization code