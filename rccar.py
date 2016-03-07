"""
This class controls the RC car itself. It's intended to be the real-world
version of the carmunk simulation.
"""
import RPi.GPIO as GPIO
import time
import numpy as np
import socket

# Constants
LEFT_PIN = 13
RIGHT_PIN = 15
FORWARD_PIN = 12
BACKWARD_PIN = 11
ITER_PAUSE = 1  # Time to pause between actions for observation.
MOVE_DURATION = 0.15  # Time to apply forward/backward force.
STEERING_DELAY = 0.5  # Time to wait after we move before straightening.

# Used for getting sensor readings.
HOST = '192.168.2.12'
PORT = 8888
SIZE = 1024


class RCCar:
    def __init__(self):
        print("Setting up GPIO pins.")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(BACKWARD_PIN, GPIO.OUT)  # Backwards.
        GPIO.setup(FORWARD_PIN, GPIO.OUT)  # Forwards.
        GPIO.setup(LEFT_PIN, GPIO.OUT)  # Left.
        GPIO.setup(RIGHT_PIN, GPIO.OUT)  # Right.

        # Just to make sure.
        GPIO.output(BACKWARD_PIN, 0)
        GPIO.output(FORWARD_PIN, 0)
        GPIO.output(LEFT_PIN, 0)
        GPIO.output(RIGHT_PIN, 0)

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
        Call our server on the other Pi to get the readings.
        """
        # Connect to our server to get the reading.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        readings = s.recv(SIZE)
        s.close()

        # Turn our crazy string into an actual list.
        readings = readings.decode('utf-8')
        readings = readings[1:-1]
        readings = readings.split(', ')

        readings = [int(float(i)) for i in readings]

        # The max value in training is 39, so let's reduce to see
        # what happens.
        reduced_readings = []
        for reading in readings:
            if reading > 39:
                reading = 39
            reduced_readings.append(reading)
        return np.array([reduced_readings])

    def recover(self):
        # Back up and turn to the left to try to get away from the obstacle.
        self.perform_action(0, True)

    def perform_action(self, action, reverse=False):
        print("Performing an action: %d" % action)
        if action == 0:  # Turn left.
            GPIO.output(LEFT_PIN, 1)
        elif action == 1:  # Turn right.
            GPIO.output(RIGHT_PIN, 1)

        # Now that the wheel is turned (or not), move a bit.
        if reverse:
            GPIO.output(BACKWARD_PIN, 1)
        else:
            GPIO.output(FORWARD_PIN, 1)

        # Pause...
        time.sleep(MOVE_DURATION)

        # Now turn off the power.
        GPIO.output(BACKWARD_PIN, 0)
        GPIO.output(FORWARD_PIN, 0)

        # Wait a bit longer before turning off the direction.
        time.sleep(STEERING_DELAY)
        GPIO.output(LEFT_PIN, 0)
        GPIO.output(RIGHT_PIN, 0)

        # Pause just to see what's going on.
        time.sleep(ITER_PAUSE)

    def car_is_crashed(self, readings):
        # If any of the readings show less than 5cm, we're crashed.
        for reading in readings[0]:
            if reading < 5:
                return True
        return False


if __name__ == '__main__':
    pass
