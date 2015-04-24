import warnings
import matplotlib as mpl
from pylab import *
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from pandas import DataFrame, Series
    import pandas as pd

userFrame = pd.read_pickle(
    "savedFrames/summaryStatistics/userTable")
reviewerFrame = pd.read_pickle(
    "savedFrames/summaryStatistics/reviewerTable")
papersFrame = pd.read_pickle(
    "savedFrames/summaryStatistics/papersTable")

#print userFrame.head()
#userFrame.hist()
#show()

#reviewerFrame.hist()
#papersFrame.hist()

subjectAreas = papersFrame["primarySubjectArea"]\
    .value_counts()\
    .sort_index(ascending=False)
length = len(subjectAreas)

fig = plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)
ttl = "Paper Subject Areas"

#colors
a = .8

plt.figure(1)
subjectAreas.plot(
    kind='barh',
    ax=ax,
    alpha=a,
    legend=False,
    edgecolor='w',
    xlim=(0, max(subjectAreas)),
    title=ttl
)

#remove grid lines
ax.grid(True)
#remove plot frame
ax.set_frame_on(False)
#remove lines on axis
ax.lines[0].set_visible(False)
#customize title
ax.set_title(ax.get_title(), fontsize=26, alpha=a, ha='left')
plt.subplots_adjust(top=0.9)
ax.title.set_position((0, 1.08))

#set x axis label on top of plot, set label text
ax.xaxis.set_label_position('top')
xlab = 'Primary Subject Area Counts'
ax.set_xlabel(xlab, fontsize=20, alpha=a, ha='left')
ax.xaxis.set_label_coords(0, 1.04)

#position x tick labels
ax.xaxis.tick_top()
ax.yaxis.set_ticks_position('none')
ax.xaxis.set_ticks_position('none')

for container in ax.containers:
    for i, child in enumerate(container.get_children()):
        child.set_color(mpl.cm.ocean(i*1.0/length))


plt.figure(2)

pastPaperFreq = userFrame["#PastPapers"].value_counts().hist(histtype='stepfilled')


show()
