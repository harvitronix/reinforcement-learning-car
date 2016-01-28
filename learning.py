from game import lapmaster_game
import numpy as np
import random
import tensorflow as tf

ACTIONS = 4  # Left, right, gear up, gear down.
INITIAL_EPSILON = 1.0
GAMMA = 0.99
OBSERVE = 200.
EXPLORE = 500000.
FINAL_EPSILON = 0.1
INITIAL_EPSILON = 1.0
REPLAY_MEMORY = 100000
BATCH = 100
K = 1


def train_net(s, readout, h_fc1, sess):
    # define the cost function
    a = tf.placeholder("float", [None, ACTIONS])
    y = tf.placeholder("float", [None])
    readout_action = tf.reduce_sum(tf.mul(readout, a), reduction_indices=1)
    cost = tf.reduce_mean(tf.square(y - readout_action))
    train_step = tf.train.AdamOptimizer(1e-6).minimize(cost)

    # open up a game state to communicate with emulator
    game_state = lapmaster_game.GameState()

    # store the previous observations in replay memory
    D = []

    # get the first state by doing nothing and preprocess the image to 80x80x4
    reward_0, readings = game_state.frame_step([0, 0, 0, 0])
    s_t = np.stack((readings, readings, readings, readings), axis=2)

    sess.run(tf.initialize_all_variables())

    epsilon = INITIAL_EPSILON
    t = 0
    while "bear" != "echo":
        # choose an action epsilon greedily
        readout_t = readout.eval(feed_dict={s: [s_t]})[0]
        a_t = np.zeros([ACTIONS])
        action_index = 0
        if random.random() <= epsilon or t <= OBSERVE:
            action_index = random.randrange(ACTIONS)
            a_t[random.randrange(ACTIONS)] = 1
        else:
            action_index = np.argmax(readout_t)
            a_t[action_index] = 1

        # scale down epsilon
        if epsilon > FINAL_EPSILON and t > OBSERVE:
            epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE

        # run the selected action and observe next state and reward
        reward_t, readings_t = game_state.frame_step(a_t)
        # I don't know why I'm supposed to do this.
        readings_t = np.reshape(readings_t, (8, 4, 1))
        s_t1 = np.append(readings_t, s_t[:, :, 1:], axis=2)

        # Reset the car if we go off the track.
        if reward_t < 0:
            game_state = lapmaster_game.GameState()

        # store the transition in D
        D.append((s_t, a_t, reward_t, s_t1, 0))
        if len(D) > REPLAY_MEMORY:
            D.pop(0)

        # only train if done observing
        if t > OBSERVE:
            # sample a minibatch to train on
            minibatch = random.sample(D, BATCH)

            # get the batch variables
            s_j_batch = [d[0] for d in minibatch]
            a_batch = [d[1] for d in minibatch]
            r_batch = [d[2] for d in minibatch]
            s_j1_batch = [d[3] for d in minibatch]

            y_batch = []
            readout_j1_batch = readout.eval(feed_dict={s: s_j1_batch})
            for i in range(0, len(minibatch)):
                # if terminal only equals reward
                if minibatch[i][4]:
                    y_batch.append(r_batch[i])
                else:
                    y_batch.append(
                        r_batch[i] + GAMMA * np.max(readout_j1_batch[i])
                    )

            # perform gradient step
            train_step.run(feed_dict={
                y: y_batch,
                a: a_batch,
                s: s_j_batch})

        # update the old values
        s_t = s_t1
        t += K

        # print info
        state = ""
        if t <= OBSERVE:
            state = "observe"
        elif t > OBSERVE and t <= OBSERVE + EXPLORE:
            state = "explore"
        else:
            state = "train"

        print("TIMESTEP", t, "/ STATE", state, "/ EPSILON", epsilon,
              "/ ACTION", action_index, "/ REWARD", reward_t, "/ Q_MAX %e"
              % np.max(readout_t))


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.01)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.01, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W, stride):
    return tf.nn.conv2d(x, W, strides=[1, stride, stride, 1], padding="SAME")


def max_pool_2x2(x):
    return tf.nn.max_pool(
        x,
        ksize=[1, 2, 1, 1],
        strides=[1, 1, 1, 1],
        padding="SAME"
    )


def conv_net():
    # network weights
    W_conv1 = weight_variable([8, 4, 4, 32])
    b_conv1 = bias_variable([32])

    W_conv2 = weight_variable([2, 1, 32, 64])
    b_conv2 = bias_variable([64])

    W_conv3 = weight_variable([2, 1, 64, 64])
    b_conv3 = bias_variable([64])

    W_fc1 = weight_variable([64, 64])
    b_fc1 = bias_variable([64])

    W_fc2 = weight_variable([64, ACTIONS])
    b_fc2 = bias_variable([ACTIONS])

    # input layer
    s = tf.placeholder("float", [None, 8, 4, 4])

    # hidden layers
    h_conv1 = tf.nn.relu(conv2d(s, W_conv1, 4) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2, 1) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    h_conv3 = tf.nn.relu(conv2d(h_pool2, W_conv3, 1) + b_conv3)
    h_pool3 = max_pool_2x2(h_conv3)

    h_pool3_flat = tf.reshape(h_pool3, [-1, 64])

    h_fc1 = tf.nn.relu(tf.matmul(h_pool3_flat, W_fc1) + b_fc1)

    # readout layer
    readout = tf.matmul(h_fc1, W_fc2) + b_fc2

    return s, readout, h_fc1

if __name__ == "__main__":
    sess = tf.InteractiveSession()
    s, readout, h_fc1 = conv_net()
    train_net(s, readout, h_fc1, sess)
