import warnings
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
    import numpy as np
from sklearn.linear_model import lars_path
from sklearn import cross_validation
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
import random
import math


df = pd.read_pickle(
    "savedFrames/predictionFeatures/paperTable")
df["binaryKDD"] = (df["maxKDDPaperCount"] > 0) + 0
df["binaryNIPS"] = (df["maxNIPSPaperCount"] > 0) + 0
df["binarySIGIR"] = (df["maxSIGIRPaperCount"] > 0) + 0
df["binarySIGMOD"] = (df["maxSIGMODPaperCount"] > 0) + 0
df["binaryICML"] = (df["maxICMLPaperCount"] > 0) + 0
df["binaryICDE"] = (df["maxICDEPaperCount"] > 0) + 0
df["binaryICDM"] = (df["maxICDMPaperCount"] > 0) + 0
features = [
    # "maxPaperCountLog",
    # "maxTopPaperCountLog",
    # "maxConnectivityLog",
    # "maxPageRankLog",
    # "maxDegCentralityLog",
    # "numAuthorsLog",
    "maxKDDPaperCountLog",
    "maxNIPSPaperCountLog",
    "maxSIGIRPaperCountLog",
    "maxSIGMODPaperCountLog",
    "maxICMLPaperCountLog",
    "maxICDEPaperCountLog",
    "maxICDMPaperCountLog",
]
features2 = [
    "binaryKDD",
    "binaryNIPS",
    "binarySIGIR",
    "binarySIGMOD",
    "binaryICML",
    "binaryICDM",
]
X = df[features]
y = df["avgRating"]

alphas, unused, coefs = lars_path(1.0*X.values, y.values, method='lasso', verbose=True)

plt.figure()
lines = plt.plot(alphas, coefs.T, linewidth=2.0)
plt.xlabel('Regularization Parameter')
plt.ylabel('Coefficients')
plt.title('LASSO Path')
leg = plt.legend(iter(lines), ('KDD', 'NIPS', 'SIGIR', 'SIGMOD', 'ICML', 'ICDE', 'ICDM'),loc=1)
for legobj in leg.legendHandles:
    legobj.set_linewidth(2.0)

X = df[features2]
alphas, unused, coefs = lars_path(1.0*X.values, y.values, method='lasso', verbose=True)

plt.figure()
lines = plt.plot(alphas, coefs.T, linewidth=2.0)
plt.xlabel('Regularization Parameter')
plt.ylabel('Coefficients')
plt.title('LASSO Path')
leg = plt.legend(iter(lines), ('KDD', 'NIPS', 'SIGIR', 'SIGMOD', 'ICML', 'ICDE', 'ICDM'),loc=1)
for legobj in leg.legendHandles:
    legobj.set_linewidth(2.0)


plt.show()
