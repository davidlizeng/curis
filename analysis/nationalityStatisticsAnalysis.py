import warnings
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
from utilities.plotBucket import plotBucket
from utilities.plotBucket import plotBar
from scipy import stats
from scipy.interpolate import spline
import snap
import codecs
import datetime

df_rating = pd.read_pickle(
    "savedFrames/ratingPrediction/ratingTable")
df_paper = pd.read_pickle(
    "savedFrames/summaryStatistics/papersTable")
df_reviewer = pd.read_pickle(
    "savedFrames/summaryStatistics/reviewerTable")
df_user = pd.read_pickle(
    "savedFrames/summaryStatistics/userTable")
df_dist = pd.read_pickle(
    "savedFrames/reviewStatistics/reviewTable")
df_mostSimilar = pd.read_pickle(
    "savedFrames/ratingPrediction/mostSimilarTable")
df_merged = pd.merge(df_rating, df_dist, on=['paperId', 'userId', 'rating'])
df_merged = pd.merge(df_merged, df_mostSimilar, on=['paperId'])


# df_rating['time'] = df_rating['time'].values.astype(datetime.datetime)
# bins = np.percentile(df_rating['time'], [0, 20, 40, 60, 80, 100])
# means = []
# labels = ['3/20', '3/30', '4/10', '4/20', '4/30']
# df_rating['absRating'] = df_rating['rating'].abs()
# dates = pd.Series([np.datetime64(datetime.datetime.strptime(d + '/2014', '%m/%d/%Y')) for d in labels]).values.astype(datetime.datetime)
# for i in range(5):
#     means.append(df_rating[(df_rating['time'] >= bins[i]) & \
#         (df_rating['time'] < bins[i+1])]['rating'].mean())

# plotBucket(df_rating, 'time', 'rating', 5, x_percentile=False, title='Rating v. Submission time')
# xticks(dates, labels)
# xlabel('Date review was last updated')
# ylabel('Final rating')
# plotBucket(df_rating, 'time', 'reviewLength', 10, x_percentile=False, title='Review Length v. Submission time')
# xticks(dates, labels)
# xlabel('Date review was last updated')
# ylabel('Review length in words')
# plotBucket(df_rating, 'time', 'absRating', 10, x_percentile=False, title='Rating v. Submission time')
# xticks(dates, labels)
# xlabel('Date review was last updated')
# ylabel('Absolute value of rating')
# plotBucket(df_rating, 'time', 'reviewLength', 10, x_percentile=False, title='Review Length v. Submission time')
# xticks(dates, labels)
# xlabel('Date review was last updated')
# ylabel('Review length in words')
# xlim([dates[2], dates[3]])
# USA 164
# China 33
# Germany 27
# Singapore 14
# Taiwan 10
# Japan 9
# Canada 9
# Italy 9
# Australia 9

# USA               1387
# China              428
# Australia          120
# Canada             111
# Japan              108
# India              103
# Germany             75
# Taiwan              65

reviewerCountries = sorted(['USA', 'China', 'Germany'])
authorCountries = sorted(['USA', 'China', 'Australia', 'Canada', 'Japan', 'India', 'Germany'])
commonCountryRatings = df_rating[df_rating['reviewerCountry'].isin(reviewerCountries) &
    df_rating['authorCountryMode'].isin(authorCountries)]
ratingsByCountry = commonCountryRatings.groupby(['reviewerCountry','authorCountryMode'])['rating'].mean().unstack()
countsByCountry = commonCountryRatings.groupby(['reviewerCountry'])['authorCountryMode'].value_counts().unstack()
meansByCountry = commonCountryRatings.groupby(['authorCountryMode'])['rating'].mean()
fig, ax = plt.subplots()
xvalues = np.arange(len(authorCountries))
colors = ['b', 'r', 'g']
markers = ['o', 's', 'd']
ix = np.argsort(meansByCountry)
for i in range(len(reviewerCountries)):
    ax.plot(xvalues + (i - 1)*0.01, [ratingsByCountry.ix[reviewerCountries[i]].values[j] for j in ix],
        color = colors[i], marker = markers[i], label = reviewerCountries[i], linewidth='2', alpha=0.7)
ax.plot(xvalues, [meansByCountry.values[j] for j in ix], color = 'k', linestyle = ':', marker = 'x', label='mean', alpha=0.7, linewidth='3')
ax.plot(plt.xlim(),[df_rating['rating'].mean(), df_rating['rating'].mean()], color='k', linestyle='--')
ax.set_xticks(np.arange(len(authorCountries)), minor=False)
ax.set_xticklabels([authorCountries[j] for j in ix], minor=False)
plt.legend(loc=4, title='Reviewer Nationality')
plt.ylabel('Average Rating')
plt.xlabel('Mode Author Nationality of Paper')
plt.title('Rating vs. Nationalities')
commonAuthor = df_rating[df_rating['authorCountryMode'].isin(authorCountries)]
submissions = commonAuthor.groupby('authorCountryMode').size()
sortedSubs = [submissions.values[j] for j in ix]
for i in range(len(sortedSubs)):
  plt.text(xvalues[i], 0.6, sortedSubs[i], color="gray", ha="center")
plt.text(3, 0.5, "(Number of Submissions)", color="gray", ha="center")
plt.ylim([-2, 0.75])

# # USA               496
# # China             118
# # Canada             43
# # India              40
# # Australia          37
# # Japan              34
# # Germany            26

# fig, ax = plt.subplots()
# modeCountry = df_paper[df_paper['authorCountryMode'].isin(authorCountries)].groupby(['authorCountryMode'])
# maxCountry = df_paper[df_paper['maxAuthorCountry'].isin(authorCountries)].groupby(['maxAuthorCountry'])
# modeCountryMean = modeCountry['accepted'].mean()
# modeCountrySize = modeCountry.size()
# maxCountryMean = maxCountry['accepted'].mean()
# maxCountrySize = maxCountry.size()
# modeCountryError = np.sqrt(modeCountryMean*(1 - modeCountryMean)/modeCountrySize)
# maxCountryError = np.sqrt(maxCountryMean*(1 - maxCountryMean)/maxCountrySize)

# ix = np.argsort(modeCountryMean.values)
# ax.bar(xvalues - 0.2, [modeCountryMean.values[j] for j in ix],
#     width=0.4, alpha=.8, color=['#ccccff', '#ffccff', '#ffcccc', '#ccffff', '#ccffcc', '#ffffcc', '#dddddd'])
# ax.bar(xvalues, [maxCountryMean.values[j] for j in ix], yerr=[maxCountryError.values[j] for j in ix],
#     width=0.3, alpha=.8, color='g', ecolor='k', label='Most Exp Authors')
# ax.bar(xvalues + 0.1, [pAcceptByPriCountry.values[j] for j in ix], width=0.2, color='r', label='Primary Author')
# ax.plot(plt.xlim(),[df_paper['accepted'].mean(), df_paper['accepted'].mean()], color='k', linestyle='--')
# ax.set_xticks(np.arange(len(authorCountries)), minor=False)
# ax.set_xticklabels([authorCountries[j] for j in ix], minor=False)
# plt.legend(loc=2)
# plt.ylabel('Proportion Accepted')
# plt.xlabel('Mode Author Nationality')
# plt.title('Proportion of Papers Accepted Given Nationalities')

# usAuthorUsReviewer = df_rating[(df_rating['authorCountryMode'] == 'USA') & (df_rating['reviewerCountry'] == 'USA')]['rating']
# intAuthorUsReviewer = df_rating[(df_rating['authorCountryMode'] != 'USA') & (df_rating['reviewerCountry'] == 'USA')]['rating']
# usAuthorIntReviewer = df_rating[(df_rating['authorCountryMode'] == 'USA') & (df_rating['reviewerCountry'] != 'USA')]['rating']
# intAuthorIntReviewer = df_rating[(df_rating['authorCountryMode'] != 'USA') & (df_rating['reviewerCountry'] != 'USA')]['rating']

# print 'US Paper, US vs. I11l Reviewer t-test:', stats.ttest_ind(usAuthorUsReviewer, usAuthorIntReviewer)
# print 'I11l Paper, US vs. I11l Reviewer t-test:', stats.ttest_ind(intAuthorUsReviewer, intAuthorIntReviewer)
# print 'US Reviewer, US vs. I11l Paper t-test:', stats.ttest_ind(usAuthorUsReviewer, intAuthorUsReviewer)
# print 'I11l Reviewer, US vs. I11l Paper t-test:', stats.ttest_ind(usAuthorIntReviewer, intAuthorIntReviewer)

# acOrIndMean = df_paper.groupby('academicOrIndustry')['accepted'].mean()
# acOrIndSize = df_paper.groupby('academicOrIndustry').size()
# acOrIndError = np.sqrt(acOrIndMean * (1 - acOrIndMean) / acOrIndSize)
# fig, ax = plt.subplots()
# ax.bar(np.arange(3) + 0.25, acOrIndMean, yerr=acOrIndError, width=0.5, alpha=0.8, color='r', ecolor='k')
# ax.plot(plt.xlim(),[df_paper['accepted'].mean(), df_paper['accepted'].mean()], color='k', linestyle='--')
# ax.set_xticks(np.arange(3) + 0.5, minor=False)
# ax.set_xticklabels(['Academic', 'Industry', 'Mixed'])
# plt.ylabel('p(Accept)')
# plt.xlabel('Author Affiliations')
# plt.title('Probability Paper is Accepted Given Author Affiliations')

# acOrIndMean = df_rating.groupby('paperAcademicOrIndustry')['rating'].mean()
# acOrIndSize = df_rating.groupby('paperAcademicOrIndustry').size()
# acOrIndError = df_rating.groupby('paperAcademicOrIndustry')['rating'].std()/np.sqrt(acOrIndSize)
# fig, ax = plt.subplots()
# ax.bar(np.arange(3) + 0.25, acOrIndMean, yerr=acOrIndError, width=0.5, alpha=0.8, color=['#ccffcc', '#ccffff', '#ffcccc'], ecolor='k')
# ax.plot(plt.xlim(),[df_rating['rating'].mean(), df_rating['rating'].mean()], color='k', linestyle='--')
# ax.set_xticks(np.arange(3) + 0.5, minor=False)
# ax.set_xticklabels(['Academic', 'Industry', 'Mixed'])
# plt.ylabel('Rating')
# plt.title('Average Rating Given Author Affiliations')
# for i in range(len(acOrIndSize.values)):
#   plt.text(i + 0.5, -0.96, acOrIndSize.values[i], color="gray", ha="center")
# plt.text(1.5, -0.92, "(Number of Submissions)", color="gray", ha="center")
# plt.ylim([-1, 0])

# acOrIndMean = df_rating.groupby('paperAcademicOrIndustry')['reviewerRatingDiff'].mean()
# acOrIndSize = df_rating.groupby('paperAcademicOrIndustry').size()
# acOrIndError = df_rating.groupby('paperAcademicOrIndustry')['reviewerRatingDiff'].std()/np.sqrt(acOrIndSize)
# fig, ax = plt.subplots()
# ax.bar(np.arange(3) + 0.25, acOrIndMean, yerr=acOrIndError, width=0.5, alpha=0.8, color='r', ecolor='k')
# ax.plot(plt.xlim(),[df_rating['reviewerRatingDiff'].mean(), df_rating['reviewerRatingDiff'].mean()], color='k', linestyle='--')
# ax.set_xticks(np.arange(3) + 0.5, minor=False)
# ax.set_xticklabels(['Academic', 'Industry', 'Mixed'])
# plt.ylabel('Deviation')
# plt.xlabel('Author Affiliations')
# plt.title('Deviation from Reviewer Avg Given Author Affiliations')

# academic = df_user[df_user['isAcademic']]
# industry = df_user[~df_user['isAcademic']]
# fig, ax = plt.subplots()
# aHist, bins = np.histogram(academic['#PastPapers'].values, bins=[0, 1, 2, 5, 10, 20, 40, 80, 160, 320, 640, 1000])
# iHist, bins = np.histogram(industry['#PastPapers'].values, bins=[0, 1, 2, 5, 10, 20, 40, 80, 160, 320, 640, 1000])
# xvalues = np.arange(bins.shape[0] - 1)
# ax.plot(xvalues, aHist/(1.0*academic.shape[0]), marker = 'o', color='g', label='Academia')
# ax.plot(xvalues, iHist/(1.0*industry.shape[0]), marker = 'o', color='b', label='Industry')
# ax.set_xticks(np.arange(bins.shape[0]) - 0.5, minor=False)
# ax.set_xticklabels(bins, minor=False)
# plt.ylabel('Proportion of Users')
# plt.xlabel('Past Papers Published')
# plt.title('Distrbution for Experience of KDD 2014 Users')
# plt.legend(loc=1)

# academic = df_paper[df_paper['academicOrIndustry'] == 'Academic']
# industry = df_paper[df_paper['academicOrIndustry'] == 'Industry']
# mixed = df_paper[df_paper['academicOrIndustry'] == 'Mixed']
# fig, ax = plt.subplots()
# aHist, bins = np.histogram(academic['authorsPastPaperCount']/academic['#Authors'],
#     bins=[0, 1, 2, 5, 10, 20, 50, 100, 200, 500])
# iHist, bins = np.histogram(industry['authorsPastPaperCount']/industry['#Authors'],
#     bins=[0, 1, 2, 5, 10, 20, 50, 100, 200, 500])
# mHist, bins = np.histogram(mixed['authorsPastPaperCount']/mixed['#Authors'],
#     bins=[0, 1, 2, 5, 10, 20, 50, 100, 200, 500])
# xvalues = np.arange(bins.shape[0] - 1)
# ax.plot(xvalues, aHist/(1.0*academic.shape[0]), marker = 'o', color='g', label='Academia')
# ax.plot(xvalues, iHist/(1.0*industry.shape[0]), marker = 'o', color='b', label='Industry')
# ax.plot(xvalues, mHist/(1.0*mixed.shape[0]), marker = 'o', color='r', label='Mixed')
# ax.set_xticks(np.arange(bins.shape[0]) - 0.5, minor=False)
# ax.set_xticklabels(bins, minor=False)
# plt.ylabel('Proportion of Papers')
# plt.xlabel('Average Papers Published by Authors')
# plt.title('Distrbution for Experience of KDD 2014 Papers')
# plt.legend(loc=2)

# academic = df_paper[df_paper['academicOrIndustry'] == 'Academic']
# industry = df_paper[df_paper['academicOrIndustry'] == 'Industry']
# mixed = df_paper[df_paper['academicOrIndustry'] == 'Mixed']
# fig, ax = plt.subplots()
# aHist, bins = np.histogram(academic['authorsMaxPastPaper']/academic['#Authors'],
#     bins=[0, 1, 2, 5, 10, 20, 50, 100, 200, 500])
# iHist, bins = np.histogram(industry['authorsMaxPastPaper']/industry['#Authors'],
#     bins=[0, 1, 2, 5, 10, 20, 50, 100, 200, 500])
# mHist, bins = np.histogram(mixed['authorsMaxPastPaper']/mixed['#Authors'],
#     bins=[0, 1, 2, 5, 10, 20, 50, 100, 200, 500])
# xvalues = np.arange(bins.shape[0] - 1)
# ax.plot(xvalues, aHist/(1.0*academic.shape[0]), marker = 'o', color='g', label='Academia')
# ax.plot(xvalues, iHist/(1.0*industry.shape[0]), marker = 'o', color='b', label='Industry')
# ax.plot(xvalues, mHist/(1.0*mixed.shape[0]), marker = 'o', color='r', label='Mixed')
# ax.set_xticks(np.arange(bins.shape[0]) - 0.5, minor=False)
# ax.set_xticklabels(bins, minor=False)
# plt.ylabel('Proportion of Papers')
# plt.xlabel('Number of Papers Published by Most Experienced Author')
# plt.title('Distrbution for Experience of KDD 2014 Papers')
# plt.legend(loc=2)

# plt.figure()
# plt.scatter(df_user['#PastPapers'], df_user['#Siblings'], marker='o')

# reviewers = df_reviewer['userId'].values
# fin = snap.TFIn('coauthor.graph')
# graph = snap.TNEANet.Load(fin)
# dblpPaperCounts = []
# for n in graph.Nodes():
#     id = n.GetId()
#     paperCount = graph.GetIntAttrDatN(id, 'exp')
#     dblpPaperCounts.append(paperCount)

# dblpPaperCounts = np.array(dblpPaperCounts)
# nDblpPaperCounts = dblpPaperCounts
# nameToNId = {}
# usedNId = set()
# for n in graph.Nodes():
#     id = n.GetId()
#     nameToNId[graph.GetStrAttrDatN(id, 'name').decode('utf-8')] = id
# infile = codecs.open('csv/dblpusersaff.csv', 'r', 'utf-8')
# lines = infile.read().splitlines()
# infile.close()
# authorPaperCounts = []
# reviewerPaperCounts = []
# dblpUserCount = 0
# for line in lines:
#     tokens = line.split('||')
#     if tokens[2] != '':
#         nId = nameToNId[tokens[1]]
#         if nId not in usedNId:
#             usedNId.add(nId)
#             paperCount = graph.GetIntAttrDatN(nId, 'exp')
#             if int(tokens[0]) in reviewers:
#                 reviewerPaperCounts.append(paperCount)
#             else:
#                 authorPaperCounts.append(paperCount)

# nAuthorPaperCounts = np.array(authorPaperCounts)
# nReviewerPaperCounts = np.array(reviewerPaperCounts)
# dblpHist, bins  = np.histogram(nDblpPaperCounts, bins=np.logspace(0, 3, 10))
# authorHist, bins = np.histogram(nAuthorPaperCounts, bins=np.logspace(0, 3, 10))
# reviewerHist, bins2 = np.histogram(nReviewerPaperCounts, bins=np.logspace(0, 3, 7))
# nDblpHist = dblpHist/(graph.GetNodes() * 1.0)
# nAuthorHist = authorHist/((len(lines) - len(reviewers)) * 1.0)
# nReviewerHist = reviewerHist/(len(reviewers) * 1.0)

# xvals1 = (bins[:-1] + bins[1:])*0.5
# xvals2 = (bins2[:-1] + bins2[1:])*0.5

# fig = plt.figure()
# plt.plot(xvals1, nDblpHist, color='b', marker='o', label='DBLP')
# plt.plot(xvals1, nAuthorHist, color='g', marker='o', label='KDD Authors')
# plt.plot(xvals2, nReviewerHist, color='r', marker='o', label='KDD Reviewers')
# plt.semilogy()
# plt.semilogx()
# plt.xlabel('Number of Publications')
# plt.ylabel('Proportion of Total People')
# fig.suptitle('Distribution of Author Experience')
# plt.legend(loc=3)
show()
