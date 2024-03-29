# This file was created by James von Ploennies

# Goals:
# add new enemy (added, charging chihuahua)
# death (added) 
# powerups (added, increases speed)
# start screen (WIP)
# add survival timer (added)
# add waves (WIP)
# trying to make it so you can see ur time in pygame instead of console but idk how

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
        self.clock = pg.time.Clock()
        self.wave = 10000

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

        self.enemy_image = pg.image.load(path.join(images, 'chihuahua.jpg')).convert_alpha()
        self.enemy_image2 = pg.image.load(path.join(images, 'angerchihuahua.jpg')).convert_alpha()

    def new(self):
        # start all vars setup groups and instantiate classes
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.pwup = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.wavedenemies = pg.sprite.Group()
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
 
    # input
    def events(self):
        for event in pg.event.get():                                                                                   # Bruh
                if event.type == pg.QUIT:
                    self.quit()
                     
        # movement controls
                if event.type == pg.KEYDOWN:
                    if event.type == pg.QUIT:
                        self.quit()
                    # if event.key == pg.K_LEFT:
                    #     self.player.move(dx=-1)
                    # if event.key == pg.K_RIGHT:
                    #     self.player.move(dx=1)
                    # if event.key == pg.K_UP:
                    #     self.player.move(dy=-1)
                    # if event.key == pg.K_DOWN:
                    #     self.player.move(dy=1)
    # quits game
    def quit(self):
        pg.quit()
        sys.exit()
    # updates pretty much everything
    def update(self):
        self.all_sprites.update()
        if not self.players == '<Group(0 sprites)>':
            self.survtime.ticking()

    def draw_grid(self): # draws the visual grid
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGRAY, (0, y), (WIDTH, y))
    def draw(self): # draws timer sprites, and everything
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        self.draw_text(self.screen, str(self.survtime.current_time), 24, WHITE, WIDTH/2 - 32, 2)
        pg.display.flip()







    
# starts gamew
g = Game()
while True:
    g.new()
    g.run()
   

    
# instatiationa


    

s