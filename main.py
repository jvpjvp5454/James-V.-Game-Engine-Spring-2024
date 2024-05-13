# This file was created by James von Ploennies

# Goals:
# add new enemy (added, charging chihuahua)
# death (added) 
# powerups (added, increases speed)
# start screen (WIP)
# add survival timer (added)

# trying to make it so you can see ur time in pygame instead of console but idk how


# Beta Goal: Waves of enemies, or enemies that spawn after a certain amount of time (added, need to fix enemies spawning in walls but functional)
    # Also added hp and indicator when you are damaged

# Final Project Goal:
    # Boss enemy that spawns after a certain amount of time, maybe to kill it you have to get charging enemies to ram into it (dodging mechanic?), (done)
# powerup/materials that allows player to build a wall per powerup (WIP)

# Future Goals
# Enemies with varying rarities and difficulty; different every run

# More enemy types, maybe one that stuns player somehow?

# add powerup that gives dashes (done)

# Sources:
# Copilot for various different ways including corrected errors and syntax and generating code
# Tyler for help with the wave system and spawning enemies
# Stackoverflow for fixing errors


import pygame as pg 
from settings import *
from random import randint
from sprites import *
import sys
from os import path
from images import *
from math import floor
from util import *

class Game:
    # Initialization and running the game
    def __init__(self):
        pg.init
        pg.font.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.font = pg.font.Font(None, 36)  # Load a font (None = default font)
        # code borrowed from Tyler
        self.player = Player
        self.wave_timer = pg.time.get_ticks() + 20000
        print(len(self.map_data))
        self.wave = 0
        self.wave_timer_chargers = 5000

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)

    # loads saves
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        images = path.join(game_folder, 'images')
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

        self.enemy_image = pg.image.load(path.join(images, 'yellowtrirotated.png')).convert_alpha()
        self.enemy_image2 = pg.image.load(path.join(images, 'redtrirotated.png')).convert_alpha()

    def new(self):
        # start all vars setup groups and instantiate classes
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.pwup = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.wave_enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.enemychargers = pg.sprite.Group()
        self.healthkits = pg.sprite.Group()
        #self.player = Player(self, 10, 10)
        #for x in range(10, 20):
            #Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                #print(col)
                #print(tiles)
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'p':
                    self.player = Player(self, col, row)
                if tile == 't':     
                    Powerup(self, col, row)
                if tile == 'e':
                    Enemy(self,col,row)
                if tile == 'c':
                    Coin(self,col,row)
                if tile == 'x':
                    Enemy2(self,col,row)
                if tile == 'E':
                    new_enemy = Enemy(self, col, row)
                if tile == 'b':
                    Bullet(self, col ,row) # for testing purposes

                    # new_enemy.spawn(self.screen.get_width(), self.screen.get_height())
                # if tile == '2':
                #     WaitingEnemy(self,col,row)
        self.survtime = Timer(self)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
 
    # inputs
    def events(self):
        for event in pg.event.get():                                                                                 # Bruh
                if event.type == pg.QUIT: 
                    self.quit()
                     
    # code borrowed from Tyler but modified to fit my game
    def spawn_enemies(self):
        for _ in range(random.randint(0,2)):
            # col = random.randint(1, len(self.map_data[0]) - 1)  # Random column
            # row = random.randint(1, len(self.map_data) - 1)     # Random row
            # if self.map_data == '.':
            # print("I spawned enemies!" "(Hopefully)")
            x = random.randint(2,30)
            y = random.randint(2,22)
            Enemy(self, x, y)

    def spawn_chargers(self):
        for _ in range(random.randint(0,2)):
            x = random.randint(2,30)
            y = random.randint(2,22)
            Enemy2(self, x, y)
    

    def spawn_powerups(self):
        for _ in range(random.randint(1,3)):
            x = random.randint(1,30)
            y = random.randint(1,22)
            Powerup(self, x, y)
        for _ in range(random.randint(3,7)):
            x = random.randint(1,30)
            y = random.randint(1,22)
            Coin(self, x, y)
        for _ in range(random.randint(0,2)):
            x = random.randint(1,30)
            y = random.randint(1,22)
            Healthkit(self, x, y)
            #Enemy(self, col, row)
#self.screen.get_width(), self.screen.get_height())
        # movement controls
           # if event.type == pg.KEYDOWN:
              #  if event.type == pg.QUIT:
                #    self.quit()
                    # if event.key == pg.K_LEFT:
                    #     self.player.move(dx=-1)
                    # if event.key == pg.K_RIGHT:
                    #     self.player.move(dx=1)
                    # if event.key == pg.K_UP:
                    #     self.player.move(dy=-1)
                    # if event.key == pg.K_DOWN:w
                    #     self.player.move(dy=1)
    # quits game
    def quit(self):
        pg.quit()
        sys.exit()
    # updates pretty much everything
    def update(self):
        self.all_sprites.update()
        self.survtime.ticking()
        if self.wave_timer < pg.time.get_ticks():
            self.wave_timer = pg.time.get_ticks() + 20000 
            if not self.wave == 3:
                self.spawn_enemies()
            self.spawn_powerups()
            self.spawn_chargers()
            self.wave += 1
            print(self.wave)
            if self.wave == 3:  
                 self.spawn_boss()
        if self.wave_timer_chargers < pg.time.get_ticks() and self.wave == 3:
            self.wave_timer_chargers = pg.time.get_ticks() + 5000
            self.spawn_chargers()
        


    def spawn_boss(self):
        for _ in range(1):
            x = random.randint(2,30)
            y = random.randint(2,22)
            EnemyBoss(self, x, y)
          

    # def draw_grid(self): # draws the visual grid
    #     for x in range(0, WIDTH, TILESIZE):
    #         pg.draw.line(self.screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    #     for y in range(0, WIDTH, TILESIZE):
    #         pg.draw.line(self.screen, LIGHTGRAY, (0, y), (WIDTH, y))
    def draw(self): # draws timer sprites, and everything
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
    
        self.draw_text(self.screen, str(self.survtime.current_time), 24, WHITE, WIDTH/2 - 32, 2)
        dash_text = f"Dashes left: {self.player.dashes}"
        text_surface = self.font.render(dash_text, True, (255, 255, 255))  # White text
        self.screen.blit(text_surface, (0, self.screen.get_height() - text_surface.get_height()))
        pg.display.flip()



    
# starts gamew
g = Game()
while True:
    g.new()
    g.run()
   

    
# instatiationa


    

