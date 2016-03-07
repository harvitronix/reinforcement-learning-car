"""
This is the real-world equivalent of the simulation's playing.py.
"""
from nn import neural_net
import numpy as np
from rccar import RCCar


def get_model():
    saved_model = 'saved-models-driving/1000-1000-400-50000-100000.h5'
    return neural_net(3, [1000, 1000], saved_model)


def get_action_from_net(readings, model):
    return np.argmax(model.predict(readings, batch_size=1))


if __name__ == '__main__':
    print("Running.")
    model = get_model()
    car = RCCar()

    input("Net is prepped. Press enter to run.")

    print("Doing loops.")
    for i in range(50):
        readings = car.get_readings()
        print(readings)
        action = get_action_from_net(readings, model)
        car.step(action)

    car.cleanup_gpio()
