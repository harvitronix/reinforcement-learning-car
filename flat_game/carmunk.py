import random
import math
import numpy as np

import pygame
from pygame.color import THECOLORS

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
speed_multiplier = 0.02

# Showing sensors slows things down.
show_sensors = False


class GameState:
    def __init__(self):
        # Global-ish.
        self.crashed = False

        # Physics stuff.
        self.space = pymunk.Space()
        self.space.gravity = pymunk.Vec2d(0., 0.)
        self.space.add_collision_handler(1, 1, post_solve=self.car_crashed)

        # Create a car at a random corner.
        corner = random.randint(0, 3)
        if corner == 0:
            # Bottom left.
            self.create_car(100, 100, 0.5)
        elif corner == 1:
            # Top left.
            self.create_car(100, height-100, 5)
        elif corner == 2:
            # Bottom right.
            self.create_car(width-100, 100, 2.5)
        elif corner == 3:
            # Top right.
            self.create_car(width-100, height-100, 3.5)

        # To increase speed.
        self.num_steps = 0

        # Create walls.
        static = [
            pymunk.Segment(
                self.space.static_body,
                (0, 1), (0, height), 1),
            pymunk.Segment(
                self.space.static_body,
                (1, height), (width, height), 1),
            pymunk.Segment(
                self.space.static_body,
                (width-1, height), (width-1, 1), 1),
            pymunk.Segment(
                self.space.static_body,
                (1, 1), (width, 1), 1)
        ]
        for s in static:
            s.friction = 1.
            s.group = 1
            s.collision_type = 1
            s.color = THECOLORS['red']
        self.space.add(static)

        # Create some obstacles, semi-randomly.
        if random.random() > 0.5:
            self.create_obstacle(450, 350, random.randint(75, 125))
        else:
            self.create_obstacle(300, 350, random.randint(125, 150))
        if random.random() > 0.5:
            self.create_obstacle(750, 200, random.randint(75, 125))
        else:
            self.create_obstacle(750, 350, random.randint(50, 100))
        if random.random() > 0.5:
            self.create_obstacle(600, 600, random.randint(25, 50))

    def create_obstacle(self, x, y, r):
        c_body = pymunk.Body(pymunk.inf, pymunk.inf)
        c_shape = pymunk.Circle(c_body, r)
        c_shape.collision_type = 1
        c_shape.elasticity = 1.0
        c_body.position = x, y
        c_shape.color = THECOLORS["blue"]
        self.space.add(c_body, c_shape)

    def create_car(self, x, y, r):
        inertia = pymunk.moment_for_circle(1, 0, 14, (0, 0))
        self.car_body = pymunk.Body(1, inertia)
        self.car_body.position = x, y
        self.car_shape = pymunk.Circle(self.car_body, 25)
        self.car_shape.color = THECOLORS["green"]
        self.car_shape.elasticity = 1.0
        self.car_body.angle = r
        self.car_shape.collision_type = 1
        driving_direction = Vec2d(1, 0).rotated(self.car_body.angle)
        self.car_body.apply_impulse(driving_direction)
        self.space.add(self.car_body, self.car_shape)

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

        # Make it get faster over time.
        # self.car_body.velocity = (100 + self.num_steps * speed_multiplier) \
        #    * driving_direction
        self.car_body.velocity = 100 * driving_direction

        # Get the current location and the readings there.
        x, y = self.car_body.position
        readings = self.get_sensor_readings(x, y, self.car_body.angle)
        state = np.array([readings])

        # Breadcrumbs totally break its navigation.
        # if self.num_steps % 10 == 0:
        # self.drop_crumb(x, y)

        # Update the screen and stuff.
        screen.fill(THECOLORS["black"])
        draw(screen, self.space)
        self.space.step(1./10)
        pygame.display.flip()
        clock.tick()

        # Set the reward.
        if self.crashed:
            reward = -500
        else:
            reward = 30 - self.sum_readings(readings)
            # reward = 1

        self.num_steps += 1

        return reward, state

    def drop_crumb(self, x, y):
        crumb_body = pymunk.Body(pymunk.inf, pymunk.inf)
        crumb_shape = pymunk.Circle(crumb_body, 2)
        crumb_body.position = x, y
        crumb_shape.color = THECOLORS["white"]
        self.space.add(crumb_body, crumb_shape)
        # screen.set_at((int(x), int(y)), THECOLORS["white"])

    def sum_readings(self, readings):
        """Sum the number of non-zero readings."""
        tot = 0
        for i in readings:
            if i > 0:
                tot += 1  # Reduce wall reading (2) to 1.
        return tot

    def get_sensor_readings(self, x, y, angle):
        # Set a default distance.
        distance = 40

        # Get the points, as if the angle is 0.
        # We use a list because it retains order.
        sens_points = []

        # Let's try making it a big grid.
        for i in ([0, 1, 2, 3, 4, 5]):
            for j in ([-4, 4, -3, 3, -2, 2, -1, 1, 0]):
                if i == 0 and j == 0:
                    continue  # Skip the dot on top of the car.
                sens_points.append((x+(distance*j), y+(i*distance)))

        # Now rotate those to make it in the front of the car.
        # And get the observations.
        sensor_obs = []
        for point in sens_points:
            # Get the point location.
            rotated_p = self.get_rotated_point(x, y, point[0], point[1], angle)
            # Get the color there.
            if rotated_p[0] <= 0 or rotated_p[1] <= 0 \
                    or rotated_p[0] >= width or rotated_p[1] >= height:
                sensor_obs.append(2)  # Sensor is off the screen.
            else:
                obs = screen.get_at(rotated_p)
                sensor_obs.append(self.get_track_or_not(obs))
            # Now that we have the color, draw so we can see.
            if show_sensors:
                pygame.draw.circle(screen, (255, 255, 255), (rotated_p), 2)
        if show_sensors:
            pygame.display.update()

        print(sensor_obs)
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
        # Check the colors returned and convert to a 1 or a 0.
        # Reading[0] is 255 when it's red.
        # Reading[2] is 255 when it's blue.
        # Reading[1] is 255 when it's green.
        if reading == THECOLORS['blue']:
            return 1  # Sensor is on a ball.
        elif reading == THECOLORS['red']:
            return 2  # Sensor is on a wall.
        else:
            return 0
