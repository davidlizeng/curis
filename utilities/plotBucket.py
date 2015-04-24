from pylab import *
import numpy as np
import math


def plotBucket(
        df,
        xcol,
        ycol,
        delta=5,
        color="blue",
        title="default",
        x_label="default",
        y_label="default",
        x_percentile=True,
        xlim=None,
        sameFigure=False,
        marker='o',
        plotMean=True,
        ecolor=None,
        errorBars=True,
        numBuckets=None):

    setUpPlot(
        xcol, ycol, title, x_label, x_percentile, y_label, xlim, sameFigure)

    if numBuckets is not None:
        delta = 100.0/numBuckets
        percentiles = np.linspace(0, 100, numBuckets + 1).tolist()
    else:
        percentiles = range(0, 100, delta)+[100]
    col_percentiles = np.percentile(df[xcol], percentiles)

    values = []
    errors = []
    for i in range(len(percentiles) - 1):
        ratingsOfInterest = df[
            (df[xcol] >= col_percentiles[i])
            & (df[xcol] <= col_percentiles[i+1])
        ][ycol]

        values.append(ratingsOfInterest.mean())
        errors.append(
            ratingsOfInterest.std()/math.sqrt(ratingsOfInterest.shape[0])
        )

    if x_percentile:
        x = np.array(percentiles[:-1]) + (delta * .5)
    else:
        x = []
        for i in range(len(col_percentiles) - 1):
            x.append((col_percentiles[i] + col_percentiles[i+1])/2)

    if errorBars:
        p = plt.errorbar(
            x,
            values,
            marker=marker,
            color=color,
            yerr=errors,
            ecolor=ecolor,
            alpha=.8)
    else:
        p, = plt.plot(
            x,
            values,
            marker=marker,
            color=color,
            alpha=.8)

    if plotMean:
        plot(
            plt.xlim(),
            [df[ycol].mean(), df[ycol].mean()],
            color='black',
            linewidth=1,
            linestyle="--",
            alpha=.8)

    return p


def plotBar(
        df,
        xcol,
        ycol,
        x_values,
        color="blue",
        title="default",
        x_label="default",
        y_label="default",
        xlim=None,
        sameFigure=False,
        marker='o',
        plotMean=True,
        categorical=False,
        errorBars=True,
        horizontal=False):

    if horizontal:
        x_label, y_label = (y_label, x_label)

    setUpPlot(
        xcol, ycol, title, x_label, False, y_label, xlim, sameFigure)

    values = []
    errors = []
    for i in range(len(x_values)):
        ratingsOfInterest = df[df[xcol] == x_values[i]][ycol]

        values.append(ratingsOfInterest.mean())
        errors.append(
            ratingsOfInterest.std()/math.sqrt(ratingsOfInterest.shape[0])
        )

    if categorical:
        x_tickLabels = x_values
        x_values = np.arange(-.5, len(x_values)-.5, 1)

        if horizontal:
            if errorBars:
                p = plt.barh(
                    x_values,
                    values,
                    height=.9,
                    color=color,
                    xerr=errors,
                    ecolor="black"
                )
            else:
                p = plt.barh(
                    x_values,
                    values,
                    height=.95,
                    color=color
                )

            plt.ylim(-1, len(x_values))

            yticks(range(len(x_values)), x_tickLabels)

        else:
            if errorBars:
                p = plt.bar(
                    x_values,
                    values,
                    width=.95,
                    color=color,
                    yerr=errors,
                    ecolor="black"
                )
            else:
                p = plt.bar(
                    x_values,
                    values,
                    width=.95,
                    color=color
                )

            plt.xlim(-1, len(x_values))

            xticks(range(len(x_values)), x_tickLabels)

    else:
        if errorBars:
            p = plt.errorbar(
                x_values,
                values,
                marker=marker,
                color=color,
                yerr=errors)
        else:
            p, = plt.plot(
                x_values,
                values,
                marker=marker,
                color=color
            )

    if plotMean:
        if horizontal:
            plot(
                [df[ycol].mean()]*2,
                plt.ylim(),
                color='black',
                linewidth=1,
                linestyle="--")
        else:
            plot(
                plt.xlim(),
                [df[ycol].mean(), df[ycol].mean()],
                color='black',
                linewidth=1,
                linestyle="--")

    return p


def plotFrequencyHistogram(
        frame,
        col,
        xlab,
        color="Blue",
        myBins=None,
        plotMean=True):
    frame
    if myBins is not None:
        hist, bins = np.histogram(frame[col].dropna().values, myBins)
    else:
        hist, bins = np.histogram(frame[col].dropna().values)

    setUpPlot("", "",
              "Frequency Plot for "+xlab,
              xlab, False, "Count", None, False)

    width = (bins[1:] - bins[:-1])*.90
    center = (bins[:-1] + bins[1:])*1.0/2

    p = bar(
        center,
        hist,
        align='center',
        color=color,
        width=width)

    if plotMean:
        #plot average line
        plot(
            [frame[col].mean(), frame[col].mean()],
            plt.ylim(),
            color='black',
            linewidth=1,
            linestyle="--")

    for rect in p:
        height = rect.get_height()
        if height != 0:
            plt.text(rect.get_x()+rect.get_width()/2., 2+height,
                     '%d' % int(height),
                     ha='center', va='bottom')

    return p


def setUpFigure(
        x_label="",
        y_label="",
        title="",
        xlim=None,
        ipython=False):

    if ipython:
        fig = plt.figure()
    else:
        fig = plt.figure(title)
    fig.set_facecolor("white")
    plt.suptitle(title)

    xlabel(x_label)
    ylabel(y_label)

    if xlim is not None:
        plt.xlim(xlim)


def setUpPlot(
        xcol,
        ycol,
        title,
        x_label,
        x_percentile,
        y_label,
        xlim,
        sameFigure):

    if x_label == "default":
        x_label = xcol
    if y_label == "default":
        y_label = ycol
    if title == "default":
        title = y_label + " vs. " + x_label
    if x_percentile:
        x_label = x_label + " (Percentile)"

    if not sameFigure:
        setUpFigure(x_label, y_label, title, xlim)
