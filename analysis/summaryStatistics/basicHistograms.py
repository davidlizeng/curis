import warnings
import matplotlib as mpl
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd


papersFrame = pd.read_pickle(
    "savedFrames/summaryStatistics/papersTable")
userFrame = pd.read_pickle(
    "savedFrames/summaryStatistics/userTable")


def plotBasicHistogram(frame, col, xlab, color="Blue", startBins=0, bin=True):
    if (startBins > 0):
        hist, bins = np.histogram(frame[col].values, startBins)
    else:
        hist, bins = np.histogram(frame[col].values)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.set_facecolor("white")

    width = (bins[1:] - bins[:-1])*.95
    center = (bins[:-1] + bins[1:])*1.0/2

    p = ax.bar(
        center,
        hist,
        align='center',
        color=color,
        width=width)

    ax.set_title("Frequency Plot for "+xlab)
    xlabel(xlab)
    ylabel("Count")

    #plot average line
    plot(
        plt.xlim(),
        [frame[col].mean(), frame[col].mean()],
        color='black',
        linewidth=2.5,
        linestyle="--")

    for rect in p:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 10+height, '%d'%int(height),
                ha='center', va='bottom')

    return ax


plotBasicHistogram(
    userFrame,
    "#Papers",
    "Number of Submissions",
    startBins=[0,1,5,10,15,20])
show()
