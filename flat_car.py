"""
The attempts to take the original car class and make it much simpler.
No sprites, refactor the code.
"""

import pygame
import math
import random

pygame.init()
pygame.mixer.init()


class FlatCar():

    def __init__(self, screen):
        # Defaults. These really don't belong to the car. They belong
        # to the environment. Doesn't make much sense here.
        self.xs = 600
        self.ys = 450
        self.xt = self.xs - 100
        self.yt = self.ys + 100
        self.dt = 1.0  # This controls how fast the car goes. Default is 1.0.
        self.speed = 0
        self.gear = 1
        self.view = 270  # This is the angle the car is pointed.
        self.xf = 912
        self.xc = 912
        self.yc = 1410
        self.yf = 1410

        draw_car(screen)

    def update(self, screen):
        # Set speed and move it.
        self.speed = 0.95 * self.speed + .05 * (2.5 * self.gear)
        theta = self.view/57.296
        vx = self.speed * math.sin(theta)
        vy = -self.speed * math.cos(theta)
        self.xf = self.xf + vx * self.dt
        self.yf = self.yf + vy * self.dt
        self.xc = int(self.xf)
        self.yc = int(self.yf)

        # I feel like this is redundant.
        if self.view < 0:
            self.view = self.view + 360

        self.view = self.view % 360

        self.draw_car(screen)

        # Return the speed for the reward.
        return int(10.0 * self.speed)

    def draw_car(self, screen):
        # Since the car doesn't actually move, we just have to rotate it.
