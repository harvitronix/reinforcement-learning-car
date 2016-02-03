from game import lapmaster_game
import numpy as np
import random

from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import RMSprop


def train_net(model):

    observe = 5000
    epochs = 3000
    gamma = 0.975
    epsilon = 1
    batchSize = 40
    buffer = 100000
    replay = []  # stores tuples of (S, A, R, S')
    max_car_distance = 0  # Let's keep track. Each tick is a unit.
    t = 0

    for i in range(epochs):
        game_state = lapmaster_game.GameState()
        status = 1
        # 10 Sensors + the current gear.
        # state = np.array([range(11)])  # Set initial.
        # Get initial state by doing nothing and getting the state.
        _, state = game_state.frame_step((2))

        car_distance = 0  # Reset.

        while status == 1:
            t += 1
            car_distance += 1

            # We are in state S
            # Run our Q function on S to get Q values for all possible actions
            qval = model.predict(state, batch_size=1)
            # Choose an action.
            if random.random() < epsilon or t < observe:
                action = np.random.randint(0, 2)  # random
            else:
                action = (np.argmax(qval))  # best

            print(action)

            # Take action, observe new state S'
            reward, new_state = game_state.frame_step(action)

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
                    old_qval = model.predict(old_state_m, batch_size=1)
                    newQ = model.predict(new_state_m, batch_size=1)
                    maxQ = np.max(newQ)
                    y = np.zeros((0, 2))
                    y[:] = old_qval[:]
                    if reward_m > 0:  # non-terminal state
                        update = (reward_m + (gamma * maxQ))
                    else:  # terminal state
                        update = reward_m
                    y[0][action_m] = update
                    X_train.append(old_state_m.reshape(10,))
                    y_train.append(y.reshape(3,))

                X_train = np.array(X_train)
                y_train = np.array(y_train)
                print("Game #: %s" % (i,))

                model.fit(
                    X_train, y_train, batch_size=batchSize,
                    nb_epoch=1, verbose=1
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

        print("Max distance: %d at %d" % (max_car_distance, t))


def neural_net():
    model = Sequential()
    model.add(Dense(164, init='lecun_uniform', input_shape=(10,)))
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
