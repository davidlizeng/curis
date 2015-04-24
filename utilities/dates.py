import warnings
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd


def transformDates(dateLabels):
    return list(pd.Series([
        datetime.datetime.strptime(d + '/2014', '%m/%d/%Y')
        for d in dateLabels
    ]).values.astype(datetime.datetime))


def plotDeadline(yoffset=10):
    deadline = '4/15'
    plot(
        transformDates([deadline]) * 2,
        ylim(),
        color="red",
        linestyle="--",
        linewidth=2,
        alpha=.8)
    text(
        transformDates([deadline])[0],
        ylim()[1] - yoffset,
        "  Review Submission\n  Deadline",
        va="top",
        color="red",
        alpha=.8)

labels_month = ['3/20', '3/30', '4/10', '4/20', '4/30']
dates_month = transformDates(labels_month)

labels_5Days = [
    '4/10',
    '4/11',
    '4/12',
    '4/13',
    '4/14',
    '4/15',
    '4/16',
    '4/17',
]
dates_5Days = transformDates(labels_5Days)
