# This file was created by James von Ploennies

# create a player class

# create a wall class

from images import *
import time
import random 
import pygame as pg
from settings import *
from pygame.sprite import Sprite
money = 0

class Player(Sprite): # sprite class, neccesary properties such as x and y
    def __init__(self, game, x, y):
        Sprite.__init__(self)
        self.game = game
        self.groups = game.all_sprites, game.players
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE)) # sprite image?
        self.image.fill(WHITE) # color
        self.x = x * TILESIZE# position x
        self.y = y * TILESIZE# position y
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.moneybag = 0

    def get_keys(self):
        self.vx, self.vy = 0, 0

    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
                print(self.moneybag)

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

    def collide_with_powerup(self, dir):
        hits = pg.sprite.spritecollide(self, self.game.pwup, True)
        global PLAYER_SPEED
        if hits:
            PLAYER_SPEED = PLAYER_SPEED + 5
            print(PLAYER_SPEED)



    

        



    
        
          

    # def move(self, dx = 0, dy = ):
       # self.x += dx
       # self.y += dy

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def update(self):
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

        # future collision
        


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

class Powerup(Sprite):
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

class Coin(Sprite):
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

class Enemy(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.enemy_image
        #self.image.fill(RED)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect( )
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = 100, 100

    
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

    def collide_with_player(self, dir):
        hits = pg.sprite.spritecollide(self, self.game.players, True)
 
 
 
class Enemy2(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.enemy_image
        #self.image.fill(RED)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect( )
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = 100, 100

    
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

    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        cd = 0
        if cd == 0:
            if self.rect.x < self.game.player.rect.x:
                self.vx = 500
                cd == 1
                pg.time.wait(3)
                cd == 0
        if cd == 0:
            if self.rect.x > self.game.player.rect.x:
                self.vx = -500   
                cd == 1
                pg.time.wait(3)
                cd == 0 
        if cd == 0:
            if self.rect.y < self.game.player.rect.y:
                self.vy = 500
                cd == 1
                pg.time.wait(3)
                cd == 0
        if cd == 0:
            if self.rect.y > self.game.player.rect.y:
                self.vy = -500
                cd == 1
                pg.time.wait(3)
                cd == 0
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_player('x')
        self.collide_with_player('y')

    def collide_with_player(self, dir):
        hits = pg.sprite.spritecollide(self, self.game.players, True)