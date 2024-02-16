# This file was created by James von Ploennies


import pygame as pg 
from settings import *
from random import randint
from sprites import *
import sys
from os import path

def draw_text():
    pass

class Game:
    # Initialization and running the game
    def __init__(self):
        pg.init
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        pg.key.set_repeat(500, 100)
        self.load_data()

    # loads saves
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
        # start all vars setup groups and instantiate classes
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.collectables = pg.sprite.Group()
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
                    Coin(self, col, row)

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
    
    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGRAY, (0, y), (WIDTH, y))
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

g = Game()

game = Game()
# g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()
    
# instatiation

    
