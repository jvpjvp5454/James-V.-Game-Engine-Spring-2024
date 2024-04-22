# This file was created by James von Ploennies


from images import *
import time
import random 
import pygame as pg
from settings import *
from pygame.sprite import Sprite
import sys
from os import path
money = 0

dir = path.dirname(__file__)
img_dir = path.join(dir, 'images')
SPRITESHEET = "theBell.png"

game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')


class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width * 4, height * 4))
        return image
 

class Player(Sprite): # sprite class, neccesary properties such as x and y
    def __init__(self, game, x, y):
        Sprite.__init__(self)
        self.game = game
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        self.load_images() # This broke the whole game because it was in front of the self.spritesheet cpde
        self.groups = game.all_sprites, game.players
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = self.standing_frames[0]
        self.image.fill(WHITE) # color
        self.x = x * TILESIZE# position x
        self.y = y * TILESIZE# position y
        self.rect = self.image.get_rect()
        self.current_frame = 0
        self.last_update = 0
        self.material = True
        self.walking = False
        
        self.vx, self.vy = 0, 0
        self.moneybag = 0

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]
        
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
    
    def get_keys(self):
        self.vx, self.vy = 0, 0
    # kills coins and adds money
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
                print(self.moneybag)
    # changes velcoity after hitting wall
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right 
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self,self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom 
                self.vy = 0
                self.rect.y = self.y
    # increases speed and kills powerup
    def collide_with_powerup(self, dir):
        hits = pg.sprite.spritecollide(self, self.game.pwup, True)
        global PLAYER_SPEED
        if hits:
            PLAYER_SPEED = PLAYER_SPEED + 5
            print(PLAYER_SPEED)

# class Player(Sprite): # sprite class, neccesary properties such as x and y # (Old player code, keeping just in case)
#     def __init__(self, game, x, y):
#         Sprite.__init__(self)
#         self.game = game
#         self.groups = game.all_sprites, game.players
#         pg.sprite.Sprite.__init__(self, self.groups)
#         self.image = pg.Surface((TILESIZE, TILESIZE)) # sprite image?
#         self.image.fill(WHITE) # color
#         self.x = x * TILESIZE# position x
#         self.y = y * TILESIZE# position y
#         self.rect = self.image.get_rect()
#         self.vx, self.vy = 0, 0
#         self.moneybag = 0

#     def get_keys(self):
#         self.vx, self.vy = 0, 0
#     # kills coins and adds money
#     def collide_with_group(self, group, kill):
#         hits = pg.sprite.spritecollide(self, group, kill)
#         if hits:
#             if str(hits[0].__class__.__name__) == "Coin":
#                 self.moneybag += 1
#                 print(self.moneybag)
#     # changes velcoity after hitting wall
#     def collide_with_walls(self, dir):
#         if dir == 'x':
#             hits = pg.sprite.spritecollide(self, self.game.walls, False)
#             if hits:
#                 if self.vx > 0:
#                     self.x = hits[0].rect.left - self.rect.width
#                 if self.vx < 0:
#                     self.x = hits[0].rect.right 
#                 self.vx = 0
#                 self.rect.x = self.x
#         if dir == 'y':
#             hits = pg.sprite.spritecollide(self,self.game.walls, False)
#             if hits:
#                 if self.vy > 0:
#                     self.y = hits[0].rect.top - self.rect.height
#                 if self.vy < 0:
#                     self.y = hits[0].rect.bottom 
#                 self.vy = 0
#                 self.rect.y = self.y
#     # increases speed and kills powerup
#     def collide_with_powerup(self, dir):
#         hits = pg.sprite.spritecollide(self, self.game.pwup, True)
#         global PLAYER_SPEED
#         if hits:
#             PLAYER_SPEED = PLAYER_SPEED + 5
#             print(PLAYER_SPEED)



    

        



    
        
          

#     # def move(self, dx = 0, dy = ):
#        # self.x += dx
#        # self.y += dy
# # detects key presses and changes velocity
#     def get_keys(self):
#         self.vx, self.vy = 0, 0
#         keys = pg.key.get_pressed()
#         if keys[pg.K_LEFT] or keys[pg.K_a]:
#             self.vx = -PLAYER_SPEED
#         if keys[pg.K_RIGHT] or keys[pg.K_d]:
#             self.vx = PLAYER_SPEED
#         if keys[pg.K_UP] or keys[pg.K_w]:
#             self.vy = -PLAYER_SPEED
#         if keys[pg.K_DOWN] or keys[pg.K_s]:
#             self.vy = PLAYER_SPEED
#         if self.vx != 0 and self.vy != 0:
#             self.vx *= 0.7071
#             self.vy *= 0.7071

    def update(self):
        self.animate()
        #self.rect.x = self.x * TILESIZE
        #self.rect.y = self.y * TILESIZE
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.get_keys()
        self.rect.x = self.x
        self.rect.y = self.y
        self.collide_with_walls('x')
        self.collide_with_walls('y')
        self.collide_with_powerup('x')
        self.collide_with_powerup('y')
        self.collide_with_group(self.game.coins, True)

class Wall(Sprite): 
    def __init__(self, game, x, y,): # Wall class
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGRAY) # color
        self.x = x # x position
        self.y = y # y position
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.vs, self.vy = 0, 0

class Powerup(Sprite): # Powerup class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.pwup
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect( )
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.vs, self.vy = 0, 0

class Coin(Sprite): #coin class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect( )
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.vs, self.vy = 0, 0

class Enemy(Sprite): # first enemy, simple directly navigates to player
    # enemy init
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.enemy_image
        #self.image.fill(RED)
        self.rect = self.image.get_rect( )
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = 100, 100

    # checks for wall collision and redirects based on velocity
    def collide_with_walls(self, dir):
            if dir == 'x':
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                if hits:
                    self.vx *= -1
                    self.rect.x = self.x
            if dir == 'y':
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                if hits:
                    self.vy *= -1
                    self.rect.y = self.y
    # changes velocity based on position relative to player
    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        if self.rect.x < self.game.player.rect.x:
            self.vx = 110
        if self.rect.x > self.game.player.rect.x:
            self.vx = -110    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 110
        if self.rect.y > self.game.player.rect.y:
            self.vy = -110
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_player('x')
        self.collide_with_player('y')

    # checks for player collision and ends game
    def collide_with_player(self, dir):
        hits = pg.sprite.spritecollide(self, self.game.players, True)
        if hits:
            self.currenttime = pg.time.get_ticks() / 1000
            pg.quit()
            print("You survived" + str(self.currenttime) + "seconds")
            sys.exit()
 
class Enemy2(Sprite): # second enemy, slightly more complicated, charges at player and wanders around in different intervals
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.enemy_image
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = 500, 500
        self.cd = 0
        self.speedcd = 0
        
    
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y

    # same as previous but with increased speed
    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt 
        self.rect.x = self.x
        self.rect.y = self.y
        self.charge_at_player()
        self.collide_with_walls('x')
        self.collide_with_walls('y')
        self.collide_with_player('x')
        self.collide_with_player('y')
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if self.speedcd < pg.time.get_ticks() and not hits:
            self.image = self.game.enemy_image  
            if self.vy == -500:
                self.vy = -100
            if self.vy == 500:
                self.vy = 100
            if self.vx == -500:
                self.vx = -100
            if self.vx == 500:
                self.vx = 100




    # check collision and ends game
    def collide_with_player(self, dir):
        hits = pg.sprite.spritecollide(self, self.game.players, True)
        if hits:
            self.currenttime = pg.time.get_ticks() / 1000
            pg.quit()
            print("You survived " + str(self.currenttime) + "  seconds")
            sys.exit()

    # special charging script for second enemy
    def charge_at_player(self):
        if not self.cd > pg.time.get_ticks():
            self.image = self.game.enemy_image2
            if self.rect.x < self.game.player.rect.x:
                self.vx = 500
            if self.rect.x > self.game.player.rect.x:
                self.vx = -500
            if self.rect.y < self.game.player.rect.y:
                self.vy = 500
            if self.rect.y > self.game.player.rect.y:
                self.vy = -500      
            self.speedcd = pg.time.get_ticks() + 500
            self.cd = pg.time.get_ticks() + 2000

class WaitingEnemy(Sprite): # Enemy that spawns periodically, broken
    # enemy init
    def __init__(self, game, x, y):
        self.e = pg.sprite.Group
        self.gotime = pg.time.get_ticks() + 10000
        Sprite.__init__(self, self.groups)
        self.groups = game.all_sprites, game.enemies, game.wavedenemies, self.e
        self.game = game
        self.image = game.enemy_image
        #self.image.fill(RED)
        self.rect = self.image.get_rect( )
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = 100, 100

        

    # checks for wall collision and redirects based on velocity
    def collide_with_walls(self, dir):
            if dir == 'x':
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                if hits:
                    self.vx *= -1
                    self.rect.x = self.x
            if dir == 'y':
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                if hits:
                    self.vy *= -1
                    self.rect.y = self.y
    # changes velocity based on position relative to player
    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        if self.rect.x < self.game.player.rect.x:
            self.vx = 110
        if self.rect.x > self.game.player.rect.x:
            self.vx = -110    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 110
        if self.rect.y > self.game.player.rect.y:
            self.vy = -110
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_player('x')
        self.collide_with_player('y')
        if self.gotime < pg.time.get_ticks():
            self.game.wavedenemies.add()
    # checks for player collision and ends game
    def collide_with_player(self, dir):
        hits = pg.sprite.spritecollide(self, self.game.players, True)
        if hits:
            self.currenttime = pg.time.get_ticks() / 1000
            pg.quit()
            print("You survived" + str(self.currenttime) + "seconds")
            sys.exit()