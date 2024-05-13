# This file was created by James von Ploennies

print("This is the sprites script. To launch the game, run main.py.")

from images import *
import time
import random 
import pygame as pg
from settings import *
from pygame.sprite import Sprite
import math
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
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image
 

class Player(Sprite): # sprite class, neccesary properties such as x and y
    def __init__(self, game, x, y):
        Sprite.__init__(self)
        self.game = game
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))

        #self.load_images() # This broke the whole game because it was in front of the self.spritesheet 
        self.groups = game.all_sprites, game.players
        pg.sprite.Sprite.__init__(self, self.groups)
        #self.image = 'theBell.png'
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #self.standing_frames[0]
        self.image.fill(ORANGE) # color
        self.x = x * TILESIZE# position x
        self.y = y * TILESIZE# position y
        self.rect = self.image.get_rect()
        self.current_frame = 0
        self.last_update = 0
        self.material = True
        self.walking = False
        self.hp = 100
        self.dmgcd = 0
        self.flickercd = 0
        self.vx, self.vy = 0, 0
        self.moneybag = 0
        self.invurnable = False
        self.dashes = 5
        self.dashcd = 0
        self.dashstrength = 30
        self.healthtick = 0
    # def load_images(self):
    #     self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
    #                             self.spritesheet.get_image(32,0, 32, 32)]
        
    # def animate(self):
    #     now = pg.time.get_ticks()
    #     if now - self.last_update > 350:
    #         self.last_update = now
    #         self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
    #         bottom = self.rect.bottom
    #         self.image = self.standing_frames[self.current_frame]
    #         self.rect = self.image.get_rect()
    #         self.rect.bottom = bottom
    
    def get_keys(self):
        self.vx, self.vy = 0, 0
    # kills coins and adds money, now adds dashes because I am not currently using money
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
                self.dashes = self.dashes + 1
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
            PLAYER_SPEED = PLAYER_SPEED + 10
            print(PLAYER_SPEED)
            self.dashstrength = self.dashstrength + 2

    def collide_with_healthkit(self):
        hits = pg.sprite.spritecollide(self, self.game.healthkits, True)
        if hits:
            self.hp = self.hp + 10
            self.healthtick = pg.time.get_ticks() + 250

    def collide_with_powerupfreeze(self, dir): # unused because freeze is not working so i disabled it
        hits = pg.sprite.spritecollide(self, self.game.freezepwup, True)
        if hits:
            self.game.enemies.old_vx, self.game.enemies.old_vy = self.game.enemies.vx, self.game.enemies.vy  # Store old velocity
            self.game.enemies.freeze()
           
    def collide_with_bullet(self):
        hits = pg.sprite.spritecollide(self, self.game.bullets, False)
        if hits and not self.dmgcd > pg.time.get_ticks():
            self.hp = self.hp - 20
            self.dmgcd = pg.time.get_ticks() + 200

    def collide_with_bomb(self):
        pass
    
    

    def move(self, dx, dy):
       self.x += dx
       self.y += dy
# detects key presses and changes velocity
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
        if keys[pg.K_SPACE]:
            if self.vx > 0 or self.vx < 0 or self.vy > 0 or self.vy < 0:
                if not self.dashes < 1 and self.dashcd < pg.time.get_ticks():
                    if self.vy > 0:
                        self.y = self.y + self.dashstrength
                    if self.vx > 0:
                        self.x = self.x + self.dashstrength 
                    if self.vy < 0:
                        self.y = self.y - self.dashstrength
                    if self.vx < 0:
                        self.x = self.x - self.dashstrength
                    self.dashes = self.dashes - 1
                    self.dashcd = pg.time.get_ticks() + 250

        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def update(self):
        #self.animate()
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
        self.collide_with_enemy('x')
        self.collide_with_enemy('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_bullet()
        self.collide_with_healthkit()
        # self.image.fill(ORANGE)
        if self.hp < 1:
            self.currenttime = pg.time.get_ticks() / 1000
            pg.quit()
            print("You survived" + str(self.currenttime) + "seconds")
            sys.exit()
        if self.dmgcd > pg.time.get_ticks():
            self.image.fill(RED)
            if self.flickercd < pg.time.get_ticks():
                # if self.healthtick > pg.time.get_ticks():
                #     self.image.fill(GREEN)
               # else:
                self.image.fill(ORANGE) 
                self.flickercd = 200 + pg.time.get_ticks()
                
        else: 
            self.image.fill(ORANGE)

    def collide_with_enemy(self, dir):
        hits = pg.sprite.spritecollide(self, self.game.enemies, False)
        if hits and not self.dmgcd > pg.time.get_ticks():
            #if not self.invurnable == True:
            self.hp = self.hp - 10
            self.dmgcd = pg.time.get_ticks() + 200
            

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


#class PowerUpFreeze(Sprite):
  #  def __init__(self, game, x, y):
     #   Sprite.__init__(self)
      #  self.game = game
      #  self.image = pg.Surface((TILESIZE, TILESIZE))  # Replace with actual image
       # self.image.fill(RED)  # Replace with actual color
      #  self.rect = self.image.get_rect()
      #  self.x = x * TILESIZE
      #  self.y = y * TILESIZE
      #  self.rect.x = self.x
       # self.rect.y = self.y


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

    # def collide_with_bullet(self):
    #     hits = pg.sprite.spritecollide(self, self.game.bullets, True)
    #     if hits:
    #         print("get bulleted")
   
    # def update(self):
    #     self.collide_with_bullet()

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

    def update(self):
        self.collide_with_wall()

    def collide_with_wall(self):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.kill()


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

    def collide_with_wall(self):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.kill()

    def update(self):
        self.collide_with_wall()

class Healthkit(Sprite): #coin class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.healthkits
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARKGREEN)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect( )
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.vs, self.vy = 0, 0

class Enemy(Sprite): # first enemy, simply directly navigates to player
    # enemy init
    def __init__(self, game, x, y):
        #self.spawn
        self.groups = game.all_sprites, game.enemies
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.enemy_image
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE 
        self.y = y * TILESIZE
        self.angle = 0
        self.vx, self.vy = 100, 100
        self.speed = random.randint(50, 150)
        # self.player = Player
        # self.player.rect  = Player.rect

    # def freeze(self):
    #     #Freeze the enemy in place
    #     self.vx, self.vy = 0, 0  # Stop moving
    #     pg.time.set_timer(pg.USEREVENT + 1, 3000)  # Set a timer for 3 seconds

    # def unfreeze(self):
    #     #Unfreeze the enemy
    #     self.vx, self.vy = self.old_vx, self.old_vy  # Restore old velocity
    #     self.frozen = False


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
            self.vx = self.speed
        if self.rect.x > self.game.player.rect.x:
            self.vx = -1 * self.speed
        if self.rect.y < self.game.player.rect.y:
            self.vy = self.speed
        if self.rect.y > self.game.player.rect.y:
            self.vy = -1 * self.speed
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        if self.game.wave == 3:
            self.kill()
        self.angle += 1  
        self.image = pg.transform.rotate(self.game.enemy_image, self.angle)
   

    # checks for player collision and ends game
    
 
class Enemy2(Sprite): # second enemy, slightly more complicated, charges at player and wanders around in different intervals
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies, game.enemychargers
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
        self.angle = 0
        self.spincd = 0
    
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
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if self.speedcd < pg.time.get_ticks() and not hits:
            self.image = self.game.enemy_image  
            if self.vy == -400:
                self.vy = -100
            if self.vy == 400:
                self.vy = 100
            if self.vx == -400:
                self.vx = -100
            if self.vx == 400:
                self.vx = 100
         # Source: Github copilot  
        if not self.spincd > pg.time.get_ticks():
            self.angle += 1  
            self.image = pg.transform.rotate(self.game.enemy_image, self.angle)  # rotate the image
         # end of copilot code


    # def freeze(self):
    #     #Freeze the enemy in place
    #     self.vx, self.vy = 0, 0  # Stop moving
    #     pg.time.set_timer(pg.USEREVENT + 1, 3000)  # Set a timer for 3 seconds

    # def unfreeze(self):
    #     #unfreeze the enemy#
    #     self.vx, self.vy = self.old_vx, self.old_vy  # Restore old velocity
    #     self.frozen = False


    # special charging script for second enemy
    def charge_at_player(self):
        # AI gen modified code
        dx = self.game.player.rect.x - self.rect.x  # difference in x-coordinates
        dy = self.game.player.rect.y - self.rect.y  # difference in y-coordinates
        dist = math.hypot(dx, dy)  # distance between player and enemy
        self.image = pg.transform.rotate(self.game.enemy_image2, -self.angle)  # rotate the image
        # End of AI code
        if not self.cd > pg.time.get_ticks():
            self.spincd = pg.time.get_ticks() +  1500
            # produced by AI, modified to fit
            self.angle = math.atan2(dy, dx) * 180 / math.pi
            self.image = self.game.enemy_image2
            nx = dx / dist
            ny = dy / dist 
            speed = 400
            self.vx = nx * speed
            self.vy = ny * speed
            # End of AI code

            # if self.rect.x < self.game.player.rect.x:
            #     self.vx = 400
            # if self.rect.x > self.game.player.rect.x:
            #     self.vx = -400
            # if self.rect.y < self.game.player.rect.y:
            #     self.vy = 400
            # if self.rect.y > self.game.player.rect.y:
            #     self.vy = -400

            # if self.rect.x < self.game.player.rect.x:
            #     self.vx = 400
            # if self.rect.x > self.game.player.rect.x:
            #     self.vx = -400
            # if self.rect.y < self.game.player.rect.y:
            #     self.vy = 400
            # if self.rect.y > self.game.player.rect.y:
            #     self.vy = -400

            self.speedcd = pg.time.get_ticks() + 2000
            self.cd = pg.time.get_ticks() + 4000




# Boss enemy class, implemented

class EnemyBoss(Sprite): # Boss enemy, spawns bullets
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((128, 128))
        self.image.fill(LIGHTRED)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE 
        self.vx, self.vy = 500, 500
        self.hp = 800
        self.dmgcd = 0
        self.bulletcd = 0
        self.bulletbarragecd = 2000 + pg.time.get_ticks()

    def spawn_bullets(self): # making the boss shoot homing bullet
        if not self.bulletcd > pg.time.get_ticks():
            x = self.rect.x
            y = self.rect.y
            if self.vx > 0:
                Bullet(self.game, x, y, self, 300, 0)
            if self.vx < 0:
                Bullet(self.game, x, y, self, -300, 0)
            if self.vy > 0:
                Bullet(self.game, x, y, self, 0, 300)
            if self.vy < 0:
                Bullet(self.game, x, y, self, 0, -300)
            
            self.bulletcd = pg.time.get_ticks() + 1000
            print("spawned bullet")
            print(self.x)

    def spawn_bomb(self): # making the boss shoot homing bullet
        if not self.bulletcd > pg.time.get_ticks():
            x = self.rect.x
            y = self.rect.y
            if self.vx > 0:
                Bomb(self.game, x, y, self, 300, 0)
            if self.vx < 0:
                Bomb(self.game, x, y, self, -300, 0)
            if self.vy > 0:
                Bomb(self.game, x, y, self, 0, 300)
            if self.vy < 0:
                Bomb(self.game, x, y, self, 0, -300)
            
            self.bulletcd = pg.time.get_ticks() + 1000
            print("spawned bullet")
            print(self.x)

    def spawn_bullet_barrage(self): # spawns bullets all around boss at certain intervals
        if not self.bulletbarragecd > pg.time.get_ticks():
            x = self.rect.x
            y = self.rect.y
            for i in range(random.randint(3,8)):
                if random.randint(1,2) == 2:
                    Bullet(self.game, x, y, self, 300, 0)
                    Bullet(self.game, x, y, self, -300, 0)
                    Bullet(self.game, x, y, self, 0, 300)
                    Bullet(self.game, x, y, self, 0, -300)
                else:
                    Bullet(self.game, x, y, self, 300, 300)
                    Bullet(self.game, x, y, self, -300, -300)
                    Bullet(self.game, x, y, self, 300, -300)
                    Bullet(self.game, x, y, self, -300, 300)
            self.bulletbarragecd = pg.time.get_ticks() + 4000


    def collide_with_enemy2(self):
        hits = pg.sprite.spritecollide(self, self.game.enemychargers, True)
        if hits and not self.dmgcd > pg.time.get_ticks():
            self.hp = self.hp - 50
            self.dmgcd = pg.time.get_ticks() + 500
    
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
        self.collide_with_walls('x')
        self.collide_with_walls('y')
        self.collide_with_enemy2()
        self.spawn_bullets()
        self.spawn_bullet_barrage()
        hits = pg.sprite.spritecollide(self, self.game.walls, False)

        if self.dmgcd < pg.time.get_ticks():
            self.image.fill(PURPLE)
        else:
            self.image.fill(LIGHTRED)

        if self.rect.x < self.game.player.rect.x:
                    self.vx = 40
        if self.rect.x > self.game.player.rect.x:
                    self.vx = -40
        if self.rect.y < self.game.player.rect.y:
                    self.vy = 40
        if self.rect.y > self.game.player.rect.y:
                    self.vy = -40

        if self.hp < 1:
            self.kill()

class Bullet(Sprite): # bullet, shot from boss
    def __init__(self, game, x, y, boss, vx, vy):
        self.groups = game.all_sprites, game.bullets
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARKBLUE)
        self.rect = self.image.get_rect()
        self.x = x 
        self.y = y 
        # self.vx, self.vy = boss.vx * 10, boss.vy * 10
        self.vx = vx # vx and vy determined when it is spawned by boss
        self.vy = vy 


    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt 
        self.rect.x = self.x
        self.rect.y = self.y

class Bomb(Sprite): # bomb, shot from boss
    def __init__(self, game, x, y, boss, vx, vy):
        self.groups = game.all_sprites, game.bullets
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARKBLUE)
        self.rect = self.image.get_rect()
        self.x = x 
        self.y = y 
        # self.vx, self.vy = boss.vx * 10, boss.vy * 10
        self.vx = vx # vx and vy determined when it is spawned by boss
        self.vy = vy 
        self.loss = 0
        self.ticking = pg.time.get_ticks() + 5000
        self.flickercd = 0
        self.tickcount = 1000
    def tick(self):
        if self.flickercd < pg.time.get_ticks():
            self.image.fill(RED)
            self.flickercd = self.tickcount + pg.time.get_ticks()
            self.tickcount = self.tickcount - 100
            print(self.tickcount)
        else:
            self.image.fill(DARKBLUE)

    def explode(self):
        if self.tickcount < 0 or self.tickcount == 0:
            x, y = self.rect.x, self.rect.y
            BombRadius(self.game, x, y)
            self.kill()
            print("I exploded! hopefully...")


    def update(self):
        self.x += self.vx * self.game.dt 
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx, self.vy = self.vx * 0.97, self.vy * 0.97
        self.tick()
        self.explode()

class BombRadius(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.bullets
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((80, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        self.timetodie = 500

    def update(self):
        if pg.time.get_ticks() > self.timetodie:
            self.kill()


print("This is the sprites script. To launch the game, run main.py.")






# class WaitingEnemy(Sprite): # Enemy that spawns periodically and randomly, broken
#     # enemy init
#     def __init__(self, game, x, y):
#         self.e = pg.sprite.Group
#         self.gotime = pg.time.get_ticks() + 10000
#         Sprite.__init__(self, self.groups)
#         self.groups = game.all_sprites, game.enemies, game.wave_enemies, self.e
#         self.game = game
#         self.image = game.enemy_image
#         #self.image.fill(RED)
#         self.rect = self.image.get_rect( )
#         self.x = x * TILESIZE
#         self.y = y * TILESIZE
#         self.vx, self.vy = 100, 100

        

#     # checks for wall collision and redirects based on velocity
#     def collide_with_walls(self, dir):
#             if dir == 'x':
#                 hits = pg.sprite.spritecollide(self, self.game.walls, False)
#                 if hits:
#                     self.vx *= -1
#                     self.rect.x = self.x
#             if dir == 'y':
#                 hits = pg.sprite.spritecollide(self, self.game.walls, False)
#                 if hits:
#                     self.vy *= -1
#                     self.rect.y = self.y
#     # changes velocity based on position relative to player
#     def update(self):
#         self.x += self.vx * self.game.dt
#         self.y += self.vy * self.game.dt
        
#         if self.rect.x < self.game.player.rect.x:
#             self.vx = 110
#         if self.rect.x > self.game.player.rect.x:
#             self.vx = -110    
#         if self.rect.y < self.game.player.rect.y:
#             self.vy = 110
#         if self.rect.y > self.game.player.rect.y:
#             self.vy = -110
#         self.rect.x = self.x
#         self.collide_with_walls('x')
#         self.rect.y = self.y
#         self.collide_with_walls('y')
#         # if self.gotime < pg.time.get_ticks():
#         if self.gotime == 10000:
#             self.add()


#     # checks for player collision and ends game