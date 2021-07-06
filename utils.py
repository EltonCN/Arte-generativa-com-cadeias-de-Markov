import numpy as np
from matplotlib import pyplot as plt


def plot_2dhistogram(histogram, markers, name="histogram", xlabel="x", ylabel="y", save=False):
    '''
        Plots a 2d histogram from a frequency matrix

        Only works for square matrix, and with same markers in both axis

        Parameters:
            histogram: frequency matrix
            labels: labels for the axis
            name: name of the plot and of the file. Default is "histogram"
            xlabel: label for the x axis. Default is "y"
            ylabel: label for the y axis. Default is "x"
            save: True if should save the file. Default is False
    '''

    fig, ax = plt.subplots()
    im = ax.imshow(histogram, cmap="Greys", vmin = 0.0, vmax=1.0)

    if isinstance(markers, np.ndarray):
        if markers.dtype == np.float64:
            markers = np.around(markers, decimals=2)

    ax.set_xticks(np.arange(len(markers)))
    ax.set_yticks(np.arange(len(markers)))
    ax.set_xticklabels(markers)
    ax.set_yticklabels(markers)

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

    for i in range(len(markers)):
        for j in range(len(markers)):
            text = ax.text(j, i, np.around(histogram[i, j], decimals=2),
                        ha="center", va="center", color="w")


    plt.title(name)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.colorbar(im)
    plt.show()

    if save:
        fig.savefig(name+".jpg")
        