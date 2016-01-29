import pygame
from flat_car import FlatCar

screen_size = (1024, 768)
screen = pygame.display.set_mode(screen_size)
screen.fill((0, 0, 0))

clock = pygame.time.Clock()


class GameState:
    def __init__(self):
        self.car = FlatCar(screen, (0, 0), 180)
        self.gear_speed = 0        

    def frame_step(self, action):

        # Take our action and do something.
        self.act_on_car(action)

        # Get our new state.
        state = self.car.get_sensors()

        # Get our new reward, if any.
        if self.car.on_track():
            reward = self.car.speed ** 2
        else:
            reward = -500

        return reward, state

    def act_on_car(self, action):
        # Get actions.
        # Turn right.
        if action == 1:
            self.car.angle = (self.car.angle + 2) % 360
        # Turn left.
        if action == 0:
            self.car.angle = (self.car.angle + 358) % 360
        # Speed up.
        if action == 2 and self.car.speed < 100:
                self.car.speed += 1
        # Slow down.
        if action == 3 and self.car.speed > 1:
            self.car.speed -= 1

        self.car.update()


if __name__ == "__main__":
    game_state = GameState()
    while 'bear' != 'echo':
        reward, state = game_state.frame_step([1, 0, 0, 0])
        #print(reward, state)
