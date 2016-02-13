"""
Once a model is learned, use this to play it.
"""

from flat_game import carmunk
import numpy as np
from nn import neural_net

NUM_SENSORS = 53


def play(model):

    car_distance = 0
    game_state = carmunk.GameState()

    # Do nothing to get initial.
    reward, state = game_state.frame_step((2))

    # Change this to "whilte True" to make it never die.
    while reward != -500:
        car_distance += 1

        # Choose action.
        action = (np.argmax(model.predict(state, batch_size=1)))

        # Take action.
        reward, state = game_state.frame_step(action)

        # Tell us something.
        if car_distance % 1000 == 0:
            print("Current distance: %d frames." % car_distance)

    print("Made it %d frames." % car_distance)

if __name__ == "__main__":
    model = neural_net(NUM_SENSORS, True)
    play(model)
