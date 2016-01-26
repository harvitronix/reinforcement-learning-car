"""
This is from:
http://pygame.org/project-Lap+Master-2923-.html

To shift up, press up. Down, press down.
Turn left, press A. Turn right, press D.
"""

import os
import pygame
from pygame.locals import *
import car

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (8, 30)
pygame.init()
screen_size = (1024, 768)
screen = pygame.display.set_mode(screen_size)

MAX_LAPS = 10
car.MAX_LAPS = MAX_LAPS

screen.fill((0, 192, 0))

clock = pygame.time.Clock()

running = True

red = car.Sprite()
red.Load('red', 360)
car.xs = screen_size[0]/2
car.ys = screen_size[1]/2
track = pygame.image.load('track.png')
visible_track = pygame.image.load('track_textured.png')

trap = pygame.Rect(844, 1324, 140, 200)
trk = track.get_at((0, 0))

inbox = trap.collidepoint(red.xc, red.yc)
lap = 0

frames = 0
gear_lock = 24

while running:
    gear_lock = gear_lock + 1
    clock.tick(24)
    frames = frames + 1
    car.frames = frames

    #screen.fill((0,192,0))
    red.Update()
    if trap.collidepoint(red.xc,red.yc) == 0:
        if inbox == 1 :
            red.lap += 1
            inbox = 0
    else :
        inbox = 1
    screen.blit(visible_track,(car.xs-red.xc,car.ys-red.yc))
    red.Draw(car.xs,car.ys,screen)
 #   movie.make_movie(screen,frames)
    pygame.display.flip()
    onboard = True
    if red.xc >= track.get_width():
        onboard = False
    if red.xc < 0:
        onboard = False
    if red.yc >= track.get_height():
        onboard = False
    if red.yc < 0:
        onboard = False
    if onboard :
        clr = track.get_at((red.xc,red.yc))
    else :
        clr = trk
#    pdb.set_trace()
    red.wobble = 0
    if red.lap > MAX_LAPS :
        print('Total Time = ',frames/24)

        for i in range(300):
            clock.tick(24)
        exit()
    if clr == trk :
#        print 'Off track'
        red.wobble = 10
#        pdb.set_trace()
        if red.gear > 1:
            red.gear = 1
            red.speed = 1
    key = pygame.key.get_pressed()
    if red.gear > 0:
        if key[K_d] :
            red.view = (red.view+2)%360
        elif key[K_a]:
            red.view = (red.view+358)%360
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False;

            elif event.key == K_UP:
                if gear_lock > 24:
                    red.gear = red.gear + 1
                    gear_lock = 0
                    if red.gear>4 :
                        red.gear = 4
            elif event.key == K_DOWN:
                red.gear = red.gear - 1
                if red.gear < 0:
                    red.gear = 0
#            elif event.key == K_RIGHT:
#                red.view = (red.view + 2)%360
#            elif event.key == K_LEFT:
#                red.view = (red.view + 358)%360
