import sys, random

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw

width = 800
height = 600

# PyGame init
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont("Arial", 16)


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
                (25, 25), (25, height-25), 2),
            pymunk.Segment(
                self.space.static_body,
                (25, height-25), (width-25, height-25), 2),
            pymunk.Segment(
                self.space.static_body,
                (width-25, height-25), (width-25, 25), 2),
            pymunk.Segment(
                self.space.static_body,
                (25, 25), (width-25, 25), 2)
        ]

        for s in static:
            s.friction = 1.
            s.group = 1
            s.collision_type = 1
        self.space.add(static)

        # Create a rect in the middle to go around.
        box_body = pymunk.Body(pymunk.inf, pymunk.inf)
        box_shape = pymunk.Poly.create_box(box_body, (300, 200))
        box_shape.collision_type = 1
        box_shape.elasticity = 1.0
        box_body.position = 400, 300
        box_shape.color = THECOLORS["white"]
        self.space.add(box_body, box_shape)

    def car_crashed(self, space, arbiter):
        if arbiter.is_first_contact:
            for contact in arbiter.contacts:
                self.crashed = True

    def frame_step(self, action):
        if action == 0:  # Turn left.
            self.car_body.angle -= .1
        elif action == 1:  # Turn right.
            self.car_body.angle += .1

        driving_direction = Vec2d(1, 0).rotated(self.car_body.angle)
        self.car_body.velocity = 100 * driving_direction

        screen.fill(THECOLORS["black"])
        draw(screen, self.space)
        self.space.step(1./60)
        pygame.display.flip()
        clock.tick()

        if self.crashed:
            return -500
        else:
            return 1


if __name__ == '__main__':
    game_state = GameState()
    while 'bear' != 'eacho':
        reward = game_state.frame_step(random.randint(0, 3))
        if reward < 0:
            game_state = GameState()
