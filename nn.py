"""
The design of this comes from here:
http://outlace.com/Reinforcement-Learning-Part-3/
"""

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.optimizers import RMSprop


def neural_net(num_sensors, load=False):
    model = Sequential()
    model.add(Dense(164, init='lecun_uniform', input_shape=(num_sensors,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    model.add(Dense(150, init='lecun_uniform'))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    model.add(Dense(3, init='lecun_uniform'))
    model.add(Activation('linear'))

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)

    if load:
        model.load_weights('saved-models/model-weights-2794.h5')

    return model
