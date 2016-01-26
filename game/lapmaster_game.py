"""
This is from:
http://pygame.org/project-Lap+Master-2923-.html

To shift up, press up. Down, press down.
Turn left, press A. Turn right, press D.
"""

import os
import pygame
from pygame.locals import *
from . import car

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (8, 30)
screen_size = (1024, 768)
screen = pygame.display.set_mode(screen_size)
screen.fill((0, 192, 0))

clock = pygame.time.Clock()

track = pygame.image.load('./game/track.png')
visible_track = pygame.image.load('./game/track_textured.png')

trap = pygame.Rect(844, 1324, 140, 200)
trk = track.get_at((0, 0))


class GameState:

    gear_lock = 0
    frames = 0
    red = car.Sprite()
    car.xs = screen_size[0]/2
    car.ys = screen_size[1]/2

    def __init__(self):
        self.frames = 0
        self.gear_lock = 0
        self.red.Load('red', 360)

    def frame_step(self, input_array):
        """
        input_array is boolean array at:
        0: turn left
        1: turn right
        2: gear up
        3: gear down
        """
        # Set base award for this frame.
        reward = 0

        # Update stuff.
        self.gear_lock += 1
        clock.tick(24)
        self.frames += 1
        car.frames = self.frames
        current_speed = self.red.Update()

        # Move the car, I think.
        screen.blit(visible_track,
                    (car.xs - self.red.xc, car.ys - self.red.yc))
        self.red.Draw(car.xs, car.ys, screen)

        # Check if we're still on the track.
        pygame.display.flip()
        onboard = True
        if self.red.xc >= track.get_width():
            onboard = False
        if self.red.xc < 0:
            onboard = False
        if self.red.yc >= track.get_height():
            onboard = False
        if self.red.yc < 0:
            onboard = False
        if onboard:
            clr = track.get_at((self.red.xc, self.red.yc))
        else:
            clr = trk

        self.red.wobble = 0

        # Car went off the track.
        if clr == trk:
            self.red.wobble = 10
            if self.red.gear > 1:
                self.red.gear = 1
                self.red.speed = 1
            reward = -500

        # Get actions.
        if self.red.gear > 0:
            if input_array[1]:  # Turn right.
                self.red.view = (self.red.view + 2) % 360
            if input_array[0]:  # Turn left.
                self.red.view = (self.red.view + 358) % 360
            if input_array[2]:  # Gear up
                if self.gear_lock > 24 and self.red.gear < 4:
                    self.red.gear += 1
                    self.gear_lock = 0
            if input_array[3] and self.red.gear > 0:  # Gear down
                self.red.gear = self.red.gear - 1

        # Return the reward.
        if reward > 0:  # So if we haven't gone off the track.
            return current_speed
