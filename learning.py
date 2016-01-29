from game import lapmaster_game
import numpy as np
import random

from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import RMSprop


def train_net(model):

    epochs = 3000
    gamma = 0.975
    epsilon = 1
    batchSize = 40
    buffer = 80
    replay = []  # stores tuples of (S, A, R, S')
    h = 0

    for i in range(epochs):
        game_state = lapmaster_game.GameState()
        status = 1
        # 8 Sensors + the current gear.
        state = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0]])  # Set initial.

        while status == 1:
            # We are in state S
            # Run our Q function on S to get Q values for all possible actions
            qval = model.predict(state, batch_size=1)
            if (random.random() < epsilon):  # choose random action
                action = np.random.randint(0, 4)
            else:  # choose best action from Q(s,a) values
                action = (np.argmax(qval))

            # Take action, observe new state S'
            reward, new_state = game_state.frame_step(action)

            # Experience replay storage
            if (len(replay) < buffer):  # if buffer not filled, add to it
                replay.append((state, action, reward, new_state))
            else:  # if buffer full, overwrite old values
                if (h < (buffer - 1)):
                    h += 1
                else:
                    h = 0
                replay[h] = (state, action, reward, new_state)

                # Randomly sample our experience replay memory
                minibatch = random.sample(replay, batchSize)
                X_train = []
                y_train = []

                for memory in minibatch:
                    # Get max_Q(S',a).
                    old_state, action, reward, new_state = memory
                    old_qval = model.predict(old_state, batch_size=1)
                    newQ = model.predict(new_state, batch_size=1)
                    maxQ = np.max(newQ)
                    y = np.zeros((1, 4))
                    y[:] = old_qval[:]
                    if reward > 0:  # non-terminal state
                        update = (reward + (gamma * maxQ))
                    else:  # terminal state
                        update = reward
                    y[0][action] = update
                    X_train.append(old_state.reshape(9,))
                    y_train.append(y.reshape(4,))

                X_train = np.array(X_train)
                y_train = np.array(y_train)
                print("Game #: %s" % (i,))

                model.fit(
                    X_train, y_train, batch_size=batchSize,
                    nb_epoch=1, verbose=1
                )
                state = new_state
            if reward < 0:  # if reached terminal state, update game status
                status = 0

        if epsilon > 0.1:  # decrement epsilon over time
            epsilon -= (1/epochs)


def neural_net():
    model = Sequential()
    model.add(Dense(164, init='lecun_uniform', input_shape=(9,)))
    model.add(Activation('relu'))

    model.add(Dense(150, init='lecun_uniform'))
    model.add(Activation('relu'))

    model.add(Dense(4, init='lecun_uniform'))
    # linear output so we can have range of real-valued outputs
    model.add(Activation('linear'))

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)

    return model

if __name__ == "__main__":
    model = neural_net()
    train_net(model)
