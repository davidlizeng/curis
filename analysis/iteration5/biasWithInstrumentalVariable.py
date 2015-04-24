import warnings
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
    import numpy as np
from utilities.plotBucket import plotBucket
from utilities.plotBucket import plotBar
from utilities.plotBucket import plotFrequencyHistogram
from sklearn.linear_model import LinearRegression


df = pd.read_pickle(
    "savedFrames/iteration5/paperTable")

df_authors = pd.read_pickle(
	  "savedFrames/iteration5/authorTable")

col="abstractClassifierProb"

# plotBucket(
# 	df,
# 	"topPaperCountMax",
# 	"abstractClassifierProb",
# 	x_percentile=False,
# 	numBuckets=10
# )


# plotBucket(
# 	df,
# 	"topPaperCountPrimary",
# 	"abstractClassifierProb",
# 	x_percentile=False,
# 	numBuckets=10
# )

numQuantiles = 5
q = df[col].quantile(np.linspace(0,1,numQuantiles+1)).tolist()
q[numQuantiles] += .01
colors = ["red", "orange", "green", "blue", "purple"]

numQuantiles = 3
q = [0, 1.0/3, 2.0/3, 1.01]

counts = df["topPaperCountMax"]
df["paperCountPercentile"] = 100*counts.rank()/998.0
df["paperCountLog"] = log(df["topPaperCountMax"])

# p =[]

# for i in range(numQuantiles):
# 	dfTemp = df[(df[col] >= q[i]) & (df[col] < q[i+1])]
# 	p.append(plotBucket(
# 		dfTemp,
# 		"paperCountLog",
# 		"avgRating",
# 		x_percentile=False,
# 		numBuckets=7,
# 		color=colors[i],
# 		sameFigure=(i > 0),
# 		plotMean=False,
# 		x_label="Most Experienced Top Paper Count (Percentile)",
# 		y_label="Average Rating",
# 		title="Rating vs. Top Paper Count by Abstract Classifier Probability"

# 	))


# legend(
# 	p,
# 	["< 33% Acceptance Certainty", "33-66% Acceptance Certainty", ">66% Acceptance Certainty"],
# 	loc="lower right")

# for i in range(numQuantiles):
# 	dfTemp = df[(df[col] >= q[i]) & (df[col] < q[i+1])]
# 	p.append(plotBucket(
# 		dfTemp,
# 		"paperCountLog",
# 		"accepted",
# 		x_percentile=False,
# 		numBuckets=7,
# 		color=colors[i],
# 		sameFigure=(i > 0),
# 		plotMean=False,
# 		x_label="Most Experienced Top Paper Count (Percentile)",
# 		y_label="P(Accept)",
# 		title="P(Accept) vs. Top Paper Count by Abstract Classifier Probability"

# 	))


# legend(
# 	p,
# 	["< 33% Accept Cert.", "33-66% Accept Cert.", ">66% Accept Cert."],
# 	loc="upper left")

# show()
