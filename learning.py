from flat_game import carmunk
import numpy as np
import random
import csv
from collections import deque
import matplotlib.pyplot as plt
import time

from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import RMSprop

NUM_SENSORS = 30


def train_net(model):

    observe = 1000
    epochs = 5000
    gamma = 0.975
    epsilon = 1
    batchSize = 40
    buffer = 50000
    replay = []  # stores tuples of (S, A, R, S')
    max_car_distance = 0  # Let's keep track. Each tick is a unit.
    t = 0
    data_collect = []

    # For plotting.
    #plt.axis([0, epochs, 30, 300])
    #plt.ion()
    #plt.show()

    for i in range(epochs):
        # Create an empty sensor buffer that will use four frames.
        empty_sensors = [0]*NUM_SENSORS
        state = deque([empty_sensors, empty_sensors,
                      empty_sensors, empty_sensors])
        new_state = state

        # Get the game.
        game_state = carmunk.GameState()
        status = 1

        # Get initial state by doing nothing and getting the state.
        _, sensors = game_state.frame_step((2))
        state = get_buffered_state(state, sensors)

        car_distance = 0  # Reset.

        while status == 1:
            t += 1
            car_distance += 1

            # We are in state S
            # Run our Q function on S to get Q values for all possible actions
            qval = model.predict(np.array([get_flat_state(state)]),
                                 batch_size=1)

            # Choose an action.
            if random.random() < epsilon or t < observe:
                action = np.random.randint(0, 3)  # random
            else:
                action = (np.argmax(qval))  # best

            # Take action, observe new state S'
            reward, new_sensors = game_state.frame_step(action)
            new_state = get_buffered_state(new_state, new_sensors)

            # Experience replay storage
            replay.append((state, action, reward, new_state))

            # If we're done observing, start training.
            if t > observe:

                # If we've stored enough in our buffer, pop the oldest.
                if len(replay) > buffer:
                    replay.pop(0)

                # Randomly sample our experience replay memory
                minibatch = random.sample(replay, batchSize)
                X_train = []
                y_train = []

                for memory in minibatch:
                    # Get max_Q(S',a).
                    old_state_m, action_m, reward_m, new_state_m = memory
                    old_qval = model.predict(np.array([get_flat_state(old_state_m)]), batch_size=1)
                    newQ = model.predict(np.array([get_flat_state(new_state_m)]), batch_size=1)
                    maxQ = np.max(newQ)
                    y = np.zeros((1, 3))
                    y[:] = old_qval[:]
                    if reward_m > 0:  # non-terminal state
                        update = (reward_m + (gamma * maxQ))
                    else:  # terminal state
                        update = reward_m
                    y[0][action_m] = update
                    X_train.append(np.array([get_flat_state(old_state_m)]).reshape(NUM_SENSORS*4,))
                    y_train.append(y.reshape(3,))

                X_train = np.array(X_train)
                y_train = np.array(y_train)

                model.fit(
                    X_train, y_train, batch_size=batchSize,
                    nb_epoch=1, verbose=0
                )

            # Update the starting state with S'
            state = new_state

            if reward < 0:  # if reached terminal state, update game status
                status = 0
                if car_distance > max_car_distance:
                    max_car_distance = car_distance

        # decrement epsilon over time
        if epsilon > 0.1 and t > observe:
            epsilon -= (1/epochs)

        # Log the car's distance at this T
        data_collect.append([t, car_distance])
        print("Max distance: %d at %d\tgame %d\tepsilon %f" %
              (max_car_distance, t, i, epsilon))

        # Plot it.
        #plt.scatter(i, car_distance)
        #plt.draw()

    data_dump = open('learn_data.csv', 'w')
    wr = csv.writer(data_dump)
    wr.writerows(data_collect)


def get_buffered_state(state, sensors):
    """Use a queue to store four frames."""
    state.append(sensors)
    if len(state) > 4:
        state.popleft()
    return state


def get_flat_state(state):
    flat = [item for sublist in state for item in sublist]
    return flat


def neural_net():
    model = Sequential()
    model.add(Dense(164, init='lecun_uniform', input_shape=(NUM_SENSORS*4,)))
    model.add(Activation('relu'))

    model.add(Dense(150, init='lecun_uniform'))
    model.add(Activation('relu'))

    model.add(Dense(3, init='lecun_uniform'))
    # linear output so we can have range of real-valued outputs
    model.add(Activation('linear'))

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)

    return model

if __name__ == "__main__":
    model = neural_net()
    train_net(model)
