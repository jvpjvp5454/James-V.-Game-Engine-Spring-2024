import pygame as pg

clock = pg.time.Clock()

FPS = 60

frames = ["frame1", "frame2", "frame3", "frame4"]

print(len(frames))

frames_length = len(frames)

current_frame = 0
#current_frame += 1
#print(current_frame%frames_length)
#current_frame += 1
#print(current_frame%frames_length)
#current_frame += 1
#print(current_frame%frames_length)
#current_frame += 1
#print(current_frame%frames_length)
#print(frames[frames_length])


#print(current_frame%frames_length)

printme = 5 % 10
print("printed " + str(printme))

then = 0 

while True:
    #print("forever!")
    clock.tick(FPS)
    now = pg.time.get_ticks()
    if now - then > 1000:
        print(now)
        then = now
    #print(pg.time.get_ticks())
        current_frame += 1 
        print(frames[current_frame%frames_length])
        
        
#raise Exception("dog")

