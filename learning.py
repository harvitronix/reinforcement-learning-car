from flat_game import carmunk
import numpy as np
import random
import csv
from nn import neural_net

NUM_SENSORS = 44


def train_net(model):

    observe = 1000
    epochs = 1000
    gamma = 0.9
    epsilon = 1
    batchSize = 40
    buffer = 50000
    replay = []  # stores tuples of (S, A, R, S')
    max_car_distance = 0  # Let's keep track. Each tick is a unit.
    t = 0
    data_collect = []

    for i in range(epochs):
        game_state = carmunk.GameState()
        status = 1
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
                action = np.random.randint(0, 3)  # random
            else:
                action = (np.argmax(qval))  # best

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
                    y = np.zeros((1, 3))
                    y[:] = old_qval[:]
                    if reward_m > 0:  # non-terminal state
                        update = (reward_m + (gamma * maxQ))
                    else:  # terminal state
                        update = reward_m
                    y[0][action_m] = update
                    X_train.append(old_state_m.reshape(NUM_SENSORS,))
                    y_train.append(y.reshape(3,))

                X_train = np.array(X_train)
                y_train = np.array(y_train)

                model.fit(
                    X_train, y_train, batch_size=batchSize,
                    nb_epoch=1, verbose=0
                )

            # Update the starting state with S'
            state = new_state

            if reward == -500:  # if reached terminal state, update game status
                status = 0
                if car_distance > max_car_distance:
                    max_car_distance = car_distance

                    # Save the model.
                    model.save_weights('saved-models/model-weights-'
                                       + str(car_distance) + '.h5')

        # decrement epsilon over time
        if epsilon > 0.1 and t > observe:
            epsilon -= (1/epochs)

        # Log the car's distance at this T
        data_collect.append([t, car_distance])
        print("Max: %d at %d\tgame %d\tepsilon %f\t(%d)" %
              (max_car_distance, t, i, epsilon, car_distance))

    rand_filename = random.randint(1, 1000)
    data_dump = open('results/learn_data-' + str(rand_filename) + '.csv', 'w')
    wr = csv.writer(data_dump)
    wr.writerows(data_collect)


if __name__ == "__main__":
    model = neural_net(NUM_SENSORS)
    train_net(model)
