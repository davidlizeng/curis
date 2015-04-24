import warnings
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
    import numpy as np
from utilities.plotBucket import plotBucket
from utilities.plotBucket import plotBar
from utilities.plotBucket import plotFrequencyHistogram


df_paper = pd.read_pickle(
    "savedFrames/fall2014/paperTable")
df_review = pd.read_pickle(
    "savedFrames/fall2014/reviewTable")
df_reviewer = pd.read_pickle(
    "savedFrames/fall2014/reviewerTable")

#People that bid vs did not bid on papers.  Are those that bid better reviewers?
#use review length as proxy for bid quality
def f1():
	df = pd.merge(
		df_review.groupby("userId")["reviewLength"].mean().reset_index(),
		df_reviewer,
		on="userId")

	plotBucket(
		df,
		"numBids",
		"reviewLength",
		x_label="Number of Bids",
		y_label="Average Review Length",
		x_percentile=False,
		title="Review Quality vs. Number of Bids",
		numBuckets=7,
		xlim=[0,100]
	)

	plotFrequencyHistogram(
	    df,
	    'numBids',
	    'Number of Bids',
	    myBins=[0,5,10,15,20,25,30, 35, 40, 45, 50]
	)

#review variance with seniority
def f2():
	df = pd.merge(
		df_review.groupby("userId")["rating"].std().reset_index(),
		df_reviewer,
		on="userId")

	df["var"] = df["rating"] ** 2

	plotBucket(
		df,
		"dateFirstPaper",
		"var",
		x_label="Date of First Paper",
		y_label="Variance of Ratings",
		x_percentile=False,
		title="Rating Variance vs. Reviewer Seniority",
		numBuckets=5,
	)

#acceptance prob vs paper submission order
def f3():
	df = df_paper

	plotBucket(
		df,
		"paperId",
		"accepted",
		x_label="Submission Order",
		y_label="P(Accept)",
		title="Acceptance vs. Submission Order",
		numBuckets=10
	)

#how subsequent reviews influence each other
plotBar(
	df_review,
	"order",
	"rating",
	range(12)[1:],
	x_label="Review Order",
	y_label="Rating",
	title="Rating vs. Order of Review",
)

df = df_review
plots = []

colors =\
    ["red", "pink", "", "cyan", "blue",]
for i in [-2, -1, 1, 2]:
	df["rating%d" % i] = df["rating"] == i

	plots.append(plotBar(
		df_review,
		"order",
		"rating%d" % i,
		range(12)[1:],
		color = colors[i+2],
		x_label="Review Order",
		y_label="Rating Frequency",
		title="Rating Frequency vs. Order of Review",
		sameFigure= (i !=-2),
		plotMean=False
	))

legend(
	plots,
	["Reject", "Weak Reject", "Weak Accept", "Accept"],
	loc=2)

show()