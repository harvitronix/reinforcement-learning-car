from flat_game import carmunk
import numpy as np
import random
import csv
from nn import neural_net

NUM_SENSORS = 19  # The input size of our NN.
GAMMA = 0.9  # Impact of each observation on training.


def train_net(model):

    observe = 1000  # Number of frames to observe before training.
    epochs = 1000  # Number of games to play.
    epsilon = 1
    batchSize = 40
    # buffer = 50000
    buffer = 5000

    # Just stuff used below.
    max_car_distance = 0
    t = 0
    data_collect = []
    replay = []  # stores tuples of (S, A, R, S').

    for i in range(epochs):
        # Create a new game instance.
        game_state = carmunk.GameState()
        status = 1
        # Get initial state by doing nothing and getting the state.
        _, state = game_state.frame_step((2))

        car_distance = 0  # Reset.

        while status == 1:
            t += 1
            car_distance += 1

            # Get Q values for each action.
            qval = model.predict(state, batch_size=1)
            # Choose an action.
            if random.random() < epsilon or t < observe:
                action = np.random.randint(0, 3)  # random
            else:
                action = (np.argmax(qval))  # best

            # Take action, observe new state and get our treat.
            reward, new_state = game_state.frame_step(action)

            # Experience replay storage.
            replay.append((state, action, reward, new_state))

            # If we're done observing, start training.
            if t > observe:

                # If we've stored enough in our buffer, pop the oldest.
                if len(replay) > buffer:
                    replay.pop(0)

                # Randomly sample our experience replay memory
                minibatch = random.sample(replay, batchSize)

                # Get training values.
                X_train, y_train = process_minibatch(minibatch)

                # Train the model on this batch.
                model.fit(
                    X_train, y_train, batch_size=batchSize,
                    nb_epoch=1, verbose=0
                )

            # Update the starting state with S'.
            state = new_state

            # We died, so update stuff.
            if reward == -500:
                status = 0
                if car_distance > max_car_distance:
                    max_car_distance = car_distance

                    # Save the model.
                    model.save_weights('saved-models/model-weights-' +
                                       str(car_distance) + '.h5',
                                       overwrite=True)

        # Decrement epsilon over time.
        if epsilon > 0.1 and t > observe:
            epsilon -= (1/epochs)

        # Log the car's distance at this T.
        data_collect.append([t, car_distance])
        print("Max: %d at %d\tgame %d\tepsilon %f\t(%d)" %
              (max_car_distance, t, i, epsilon, car_distance))

    # Save the results to a file so we can graph it later.
    data_dump = open('results/learn_data-' + str(t) + '.csv', 'w')
    wr = csv.writer(data_dump)
    wr.writerows(data_collect)

    # Save a last version of the model.
    model.save_weights('saved-models/model-weights-'
                       + str(t) + '.h5',
                       overwrite=True)


def process_minibatch(minibatch):
    """This does the heavy lifting, aka, the training. It's super jacked"""
    X_train = []
    y_train = []
    # Loop through our batch and create arrays for X and y
    # so that we can fit our model at every step.
    for memory in minibatch:
        # Get stored values.
        old_state_m, action_m, reward_m, new_state_m = memory
        # Get prediction on old state.
        old_qval = model.predict(old_state_m, batch_size=1)
        # Get prediction on new state.
        newQ = model.predict(new_state_m, batch_size=1)
        # Get our best move. I think?
        maxQ = np.max(newQ)
        y = np.zeros((1, 3))
        y[:] = old_qval[:]
        # Check for terminal state.
        if reward_m != -500:  # non-terminal state
            update = (reward_m + (GAMMA * maxQ))
        else:  # terminal state
            update = reward_m
        # Update the value for the action we took.
        y[0][action_m] = update
        X_train.append(old_state_m.reshape(NUM_SENSORS,))
        y_train.append(y.reshape(3,))

    X_train = np.array(X_train)
    y_train = np.array(y_train)

    return X_train, y_train

if __name__ == "__main__":
    # Get the model and train our neural net!
    model = neural_net(NUM_SENSORS)
    train_net(model)
