import random
import math
import numpy as np

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw

# PyGame init
width = 1000
height = 700
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True


class GameState:
    def __init__(self):
        # Global-ish.
        self.crashed = False

        # Physics stuff
        self.space = pymunk.Space()
        self.space.gravity = pymunk.Vec2d(0., 0.)
        self.space.add_collision_handler(1, 1, post_solve=self.car_crashed)

        # Create a car.
        inertia = pymunk.moment_for_circle(1, 0, 14, (0, 0))
        self.car_body = pymunk.Body(1, inertia)
        self.car_body.position = 100, 100
        self.car_shape = pymunk.Circle(self.car_body, 30)
        self.car_shape.color = THECOLORS["green"]
        self.car_shape.elasticity = 1.0
        self.car_body.angle = 0.5
        self.car_shape.collision_type = 1
        driving_direction = Vec2d(1, 0).rotated(self.car_body.angle)
        self.car_body.apply_impulse(driving_direction)
        self.space.add(self.car_body, self.car_shape)

        # Create walls.
        static = [
            pymunk.Segment(
                self.space.static_body,
                (25, 25), (25, height-25), 25),
            pymunk.Segment(
                self.space.static_body,
                (25, height-25), (width-25, height-25), 25),
            pymunk.Segment(
                self.space.static_body,
                (width-25, height-25), (width-25, 25), 25),
            pymunk.Segment(
                self.space.static_body,
                (25, 25), (width-25, 25), 25)
        ]
        for s in static:
            s.friction = 1.
            s.group = 1
            s.collision_type = 1
            s.color = THECOLORS['blue']
        self.space.add(static)

        # Create a circle in the middle to go around.
        box_body = pymunk.Body(pymunk.inf, pymunk.inf)
        box_shape = pymunk.Circle(box_body, 100)
        box_shape.collision_type = 1
        box_shape.elasticity = 1.0
        box_body.position = 450, 350
        box_shape.color = THECOLORS["blue"]
        self.space.add(box_body, box_shape)

    def car_crashed(self, space, arbiter):
        if arbiter.is_first_contact:
            for contact in arbiter.contacts:
                self.crashed = True

    def frame_step(self, action):
        if action == 0:  # Turn left.
            self.car_body.angle -= .2
        elif action == 1:  # Turn right.
            self.car_body.angle += .2

        driving_direction = Vec2d(1, 0).rotated(self.car_body.angle)
        self.car_body.velocity = 100 * driving_direction

        x, y = self.car_body.position
        readings = self.get_sensor_readings(x, y, self.car_body.angle)
        state = np.array([readings])

        screen.fill(THECOLORS["black"])
        draw(screen, self.space)
        self.space.step(1./10)
        pygame.display.flip()
        clock.tick()

        if self.crashed:
            reward = -500
        else:
            reward = 1

        return reward, state

    def get_sensor_readings(self, x, y, angle):
        # Get a bunch of sensor points, draw them, return whether they
        # are on the track or not.

        # Set a default distance.
        distance = 45

        # Get the points, as if the angle is 0.
        # We use a list because it retains order.
        sens_points = []
        for i in ([1, 1.5, 2, 2.5, 3, 3.5]):
            sens_points.append((x+(distance*i), y))
            sens_points.append((x+(distance*i), y+(distance*i)))
            sens_points.append((x, y+(distance*i)))
            sens_points.append((x-(distance*i), y+(distance*i)))
            sens_points.append((x-(distance*i), y))

        # Now rotate those to make it in the front of the car.
        # And get the observations.
        sensor_obs = []
        for point in sens_points:
            # Get the point location.
            rotated_p = self.get_rotated_point(x, y, point[0], point[1], angle)
            # Get the color there.
            if rotated_p[0] <= 0 or rotated_p[1] <= 0 \
                    or rotated_p[0] >= width or rotated_p[1] >= height:
                sensor_obs.append(1)  # Off the screen.
            else:
                obs = screen.get_at(rotated_p)
                sensor_obs.append(self.get_track_or_not(obs))
            # Now that we have the color, draw so we can see.
            # pygame.draw.circle(screen, (255, 255, 255), (rotated_p), 2)
        # pygame.display.update()

        return sensor_obs

    def get_rotated_point(self, x_1, y_1, x_2, y_2, radians):
        radians += 1.5  # I have no idea why I have to do this.
        # Rotate x_2, y_2 around x_1, y_1 by angle.
        x_change = (x_2 - x_1) * math.cos(radians) + \
            (y_2 - y_1) * math.sin(radians)
        y_change = (y_1 - y_2) * math.cos(radians) - \
            (x_1 - x_2) * math.sin(radians)
        new_x = x_change + x_1
        new_y = height - (y_change + y_1)
        return int(new_x), int(new_y)

    def get_track_or_not(self, reading):
        # Check the colors returned and conver to a 1 or a 0.
        # Reading[2] is 255 when it's blue.
        if reading[2] == 255:
            return 1
        else:
            return 0

if __name__ == '__main__':
    game_state = GameState()
    while 'bear' != 'eacho':
        reward, readings = game_state.frame_step(random.randint(0, 3))
        if reward < 0:
            game_state = GameState()
