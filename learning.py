from game import lapmaster_game
from random import randint


def get_steer_dir():
    steering = randint(0, 3)
    steer_dir = [0, 0]
    if steering == 0:
        steer_dir = [1, 0]
    elif steering == 1:
        steer_dir = [0, 1]
    return steer_dir


def get_shift_dir():
    shifting = randint(0, 3)
    shift_dir = [0, 0]
    if shifting == 0:
        shift_dir = [1, 0]
    elif shifting == 1:
        shift_dir = [0, 1]
    return shift_dir


def play():
    target_game = lapmaster_game.GameState()
    while 'bear' != 'echo':
        action = get_steer_dir() + get_shift_dir()
        reward = target_game.frame_step(action)
        print(reward)
    
        if reward < 0:
            # Start over.
            target_game = lapmaster_game.GameState()


if __name__ == "__main__":
    play()
