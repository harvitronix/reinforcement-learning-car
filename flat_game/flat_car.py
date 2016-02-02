"""
This attempts to take the original car class and make it much simpler.
No sprites, refactor the code.
"""

import pygame
import math


class FlatCar():

    def __init__(self, screen, start_point, start_angle):
        self.speed = 10
        self.gear = 1
        self.angle = start_angle
        self.screen = screen
        self.dt = 1.0

        self.rect = pygame.Rect(start_point[0], start_point[1], 50, 100)
        pygame.draw.rect(screen, (255, 200, 0), self.rect)
        pygame.display.flip()

    def update(self):
        # Set speed and move it.
        theta = self.angle/57.296
        vx = self.speed * math.sin(theta)
        vy = -self.speed * math.cos(theta)
        self.rect.move_ip(int(vx), int(vy))
        #self.rect.x += int(vx * self.dt)
        #self.rect.y += int(vy * self.dt)
        pygame.draw.rect(self.screen, (255, 200, 0), self.rect)
        pygame.display.update()

        # I feel like this is redundant.
        if self.angle < 0:
            self.angle = self.angle + 360
        self.angle = self.angle % 360

        # Return the speed for the reward.
        return int(10.0 * self.speed)


        #pygame.display.update()

    def on_track(self):
        return True

    def get_sensors(self):
        return [0, 1, 1, 0]
