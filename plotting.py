"""
Take the data in the results folder and plot it so we can stop using stupid
Excel.
"""

import glob
import os
import csv
import matplotlib.pyplot as plt
import numpy as np

# From http://stackoverflow.com/questions/11352047/finding-moving-average-from-data-points-in-python
def movingaverage(y, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(y, window, 'same')


# Get our loss result files.
os.chdir("results")
for f in glob.glob("loss_*.csv"):
    with open(f, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # Turn our column into an array.
        y = []
        for row in reader:
            y.append(float(row[0]))

        # Get the moving average so the graph isn't so crazy.
        y_av = movingaverage(y, 100)

        # Plot it.
        plt.title(f)
        # The -50 removes an artificial drop at the end caused by the moving
        # average.
        plt.plot(y_av[:-50])
        plt.ylabel('Loss')
        plt.ylim(0, 5000)
        plt.xlim(0, 250000)
        plt.show()
        # plt.draw()

plt.show()
