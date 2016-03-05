"""
This class controls the RC car itself. It's intended to be the real-world
version of the carmunk simulation.
"""
import RPi.GPIO as GPIO
import time
import random
import numpy as np


class RCCar:
    def __init__(self):
        print("Setting up GPIO pins.")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.OUT)  # Backwards.
        GPIO.setup(12, GPIO.OUT)  # Forwards.
        GPIO.setup(13, GPIO.OUT)  # Left.
        GPIO.setup(15, GPIO.OUT)  # Right.

        # Just to make sure.
        GPIO.output(11, 0)
        GPIO.output(12, 0)
        GPIO.output(13, 0)
        GPIO.output(15, 0)

    def step(self, action):
        self.perform_action(action)

        # Now that we've moved, check/recover if crashed.
        while self.car_is_crashed(self.get_readings()):
            self.recover()

    def cleanup_gpio(self):
        print("Cleaning up GPIO pins.")
        GPIO.cleanup()

    def get_readings(self):
        """
        TODO!
        """
        readings = []
        for i in range(3):
            readings.append(random.randint(4, 14))
        print(readings)
        return np.array([readings])

    def recover(self):
        # Back up and turn to the left to try to get away from the obstacle.
        for i in range(4):
            self.perform_action(0, True)

    def perform_action(self, action, reverse=False):
        print("Performing an action: %d" % action)
        if action == 0:  # Turn left.
            GPIO.output(13, 1)
        elif action == 2:  # Turn right.
            GPIO.output(15, 1)

        # Now that the wheel is turned (or not), move a bit.
        if reverse:
            GPIO.output(11, 1)
        else:
            GPIO.output(12, 1)

        # Pause...
        time.sleep(0.1)

        # Now turn them off.
        GPIO.output(11, 0)
        GPIO.output(12, 0)
        GPIO.output(13, 0)
        GPIO.output(15, 0)

        # Pause...
        time.sleep(1)

    def car_is_crashed(self, readings):
        return False  # Debug.
        # If any of the readings show less than 5cm, we're crashed.
        for reading in readings[0]:
            if reading < 5:
                return True
        return False


if __name__ == '__main__':
    pass
