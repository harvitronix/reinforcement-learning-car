"""
This file holds a class that deals with reading from our three ultrasonic
sensors. It's called from a server, so it doesn't need to deal with
looping/reading many times. Rather, it will be called, get the readings,
and then return them.

Based on:
https://www.modmypi.com/download/range_sensor.py
"""
import RPi.GPIO as GPIO
import time

# Each sensor has a trig and echo. Order is left, middle, right | trig, echo.
PINS = [[23, 24], [25, 8], [20, 21]]


class Sensors:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        for sensor in PINS:
            GPIO.setup(sensor[0], GPIO.OUT)
            GPIO.setup(sensor[1], GPIO.IN)
            GPIO.output(sensor[0], False)

        # Wait for sensors to settle.
        print("Initializing sensors.")
        time.sleep(2)

    def get_readings(self):
        readings = []
        for sensor in PINS:
            sensor_total = 0

            # Do it three times to reduce anomolies.
            for i in range(3):
                iterations = 0

                # Blip.
                GPIO.output(sensor[0], True)
                time.sleep(0.00001)
                GPIO.output(sensor[0], False)

                # Read.
                while GPIO.input(sensor[1]) == 0 and iterations < 10000:
                    pulse_start = time.time()

                while GPIO.input(sensor[1]) == 1:
                    pulse_end = time.time()

                # Turn time into distance.
                pulse_duration = pulse_end - pulse_start
                distance = pulse_duration * 17150

                sensor_total += distance

            readings.append(round(distance / 3, 2))

        return readings

    def cleanup_gpio(self):
        GPIO.cleanup()


if __name__ == '__main__':
    sensors = Sensors()
    for i in range(100):
        print(sensors.get_readings())
        time.sleep(1)
    sensors.cleanup_gpio()
