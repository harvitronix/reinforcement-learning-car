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


def plot_file(filename, type='loss'):
    with open(f, 'r') as csvfile:
        print(f)
        reader = csv.reader(csvfile)
        # Turn our column into an array.
        y = []
        for row in reader:
            if type == 'loss':
                y.append(float(row[0]))
            else:
                y.append(float(row[1]))

        # Running tests will be empty.
        if len(y) == 0:
            return

        # Get the moving average so the graph isn't so crazy.
        if type == 'loss':
            window = 100
        else:
            window = 10
        y_av = movingaverage(y, window)

        # Use our moving average to get some metrics.
        arr = np.array(y_av)
        if type == 'loss':
            print("%f\t%f" % (arr.min(), arr.mean()))
        else:
            print("%f\t%f" % (arr.max(), arr.mean()))

        # Plot it.
        plt.clf()  # Clear.
        plt.title(f)
        # The -50 removes an artificial drop at the end caused by the moving
        # average.
        if type == 'loss':
            plt.plot(y_av[:-50])
            plt.ylabel('Smoothed Loss')
            plt.ylim(0, 5000)
            plt.xlim(0, 250000)
        else:
            plt.plot(y_av[:-5])
            plt.ylabel('Smoothed Distance')

        plt.savefig(f + '.png', bbox_inches='tight')


if __name__ == "__main__":
    # Get our loss result files.
    os.chdir("results")

    for f in glob.glob("learn*.csv"):
        plot_file(f, 'learn')

    for f in glob.glob("loss*.csv"):
        plot_file(f, 'loss')
