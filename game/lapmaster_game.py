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
import numpy as np
import sys
import math


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

    def __init__(self):
        red = car.Sprite()
        self.red = red
        self.frames = 0
        self.gear_lock = 0
        self.red.Load('red', 360)

    def frame_step(self, action):
        """
        action is an int between 0 and 3:
        0: turn left
        1: turn right
        2: gear up
        3: gear down
        """
        # Set base award for this frame.
        reward = 0

        # Update stuff.
        self.gear_lock += 1
        clock.tick()
        self.frames += 1
        car.frames = self.frames
        # reward = self.red.Update()
        # Reward is set below now (using gear instead of speed)
        self.red.Update()

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
            reward = -500  # Override the reward with a big negative.
            # Reset the car.

        # Get actions.
        if action == 1:  # Turn right.
            self.red.view = (self.red.view + 2) % 360
        if action == 0:  # Turn left.
            self.red.view = (self.red.view + 358) % 360
        if action == 2:  # Gear up
            if self.gear_lock > 24 and self.red.gear < 4:
                self.red.gear += 1
                self.gear_lock = 0
        if action == 3 and self.red.gear > 1:  # Gear down
            self.red.gear = self.red.gear - 1

        # Get the color of the screen at 8 points all around the car.
        sensor_readings = self.get_sensor_readings(
            car.xs, car.ys, self.red.view
        )

        # Add gear to sensor_readings to make a state.
        sensor_readings.append(self.red.gear)
        state = np.array([sensor_readings])

        # If we're still on the track, return the gear as the reward?
        # Will hopefully make going fast more obvious?
        if reward == 0:
            reward = self.red.gear

        # Return the reward.
        return reward, state

    def get_sensor_readings(self, x, y, angle):
        # Get a bunch of sensor points, draw them, return whether they
        # are on the track or not.

        # Assuming X/Y is the center of the car.
        distance = 50

        # Get the points, as if the angle is 0.
        # We use a list because it retains order.
        sens_points = []
        sens_points.append((x+distance, y))
        sens_points.append((x+distance, y+distance))
        sens_points.append((x, y+distance))
        sens_points.append((x-distance, y+distance))
        sens_points.append((x-distance, y))
        # Get double distance to see further.
        sens_points.append((x+distance*2, y))
        sens_points.append((x+distance*2, y+distance*2))
        sens_points.append((x, y+distance*2))
        sens_points.append((x-distance*2, y+distance*2))
        sens_points.append((x-distance*2, y))

        # Now rotate those to make it in the front of the car.
        # And get the observations.
        sensor_obs = []
        for point in sens_points:
            # Get the point location.
            rotated_p = self.get_rotated_point(x, y, point[0], point[1], angle)
            # Get the color there.
            obs = screen.get_at(rotated_p)
            sensor_obs.append(self.get_track_or_not(obs))
            # Now that we have the color, draw so we can see.
            pygame.draw.circle(screen, (255, 255, 255), (rotated_p), 2)
        pygame.display.update()

        return sensor_obs

    def get_track_or_not(self, reading):
        # Check the colors returned and conver to a 1 or a 0.
        # We ignore reading[3] because the first 3 are enough.
        if reading[0] == 128 and reading[1] == 128 and reading[2] == 0:
            return 0
        else:
            return 1

    def get_rotated_point(self, x_1, y_1, x_2, y_2, degrees):
        radians = math.radians(degrees)
        # Rotate x_2, y_2 around x_1, y_1 by angle.
        x_change = (x_2 - x_1) * math.cos(radians) + \
            (y_2 - y_1) * math.sin(radians)
        y_change = (y_1 - y_2) * math.cos(radians) - \
            (x_1 - x_2) * math.sin(radians)
        new_x = x_change + x_1
        new_y = y_change + y_1
        return int(new_x), int(new_y)
