"""
Take the data in the results folder and plot it so we can stop using stupid
Excel.
"""

import glob
import os
import csv
import matplotlib.pyplot as plt
import numpy as np


def movingaverage(y, window_size):
    """
    Moving average function from:
    http://stackoverflow.com/questions/11352047/finding-moving-average-from-data-points-in-python
    """
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(y, window, 'same')


# Get our loss result files.
os.chdir("results")
for f in glob.glob("loss*.csv"):
    with open(f, 'r') as csvfile:
        print(f)
        reader = csv.reader(csvfile)
        # Turn our column into an array.
        y = []
        for row in reader:
            y.append(float(row[0]))

        # Running tests will be empty.
        if len(y) == 0:
            continue

        # Get the moving average so the graph isn't so crazy.
        y_av = movingaverage(y, 100)

        # Use our moving average to get some metrics.
        arr = np.array(y_av)
        print("%f\t%f\t%f" % (arr.min(), arr.mean(), arr.std()))

        continue

        # Plot it.
        plt.title(f)
        # The -50 removes an artificial drop at the end caused by the moving
        # average.
        plt.plot(y_av[:-50])
        plt.ylabel('Loss/Frames')
        plt.ylim(0, 5000)
        plt.xlim(0, 250000)
        plt.show()
        # plt.draw()

# We put this here in case we used draw above, to make sure it doesn't close
# the graph until we want it to.
plt.show()
