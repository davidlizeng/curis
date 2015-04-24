import warnings
import datetime
import numpy as np
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from pandas import DataFrame


def formatDate(date):
    return\
        datetime\
        .datetime\
        .strptime(
            date.strip(),
            "%m/%d/%Y %I:%M:%S %p")

print "Importing Industry Review Data"
industryReviews = []
papers = {}

industryReviewsFile = open("csv/reviews/industry_reviews.tsv", 'r')
lines = industryReviewsFile.read().splitlines()
for line in lines:
    tokens = line.split('\t')
    paperid = int(tokens[0])
    rating = int(tokens[3])

    industryReviews.append({
        "industryId": paperid,
        "date": formatDate(tokens[1]),
        "email": tokens[2],
        "overallRating": rating,
        "comments": tokens[4],
        "privateComments": tokens[5]
    })

    if paperid not in papers:
        papers[paperid] = {}
        papers[paperid]["ratings"] = []
    papers[paperid]["ratings"].append(rating)

for id, paper in papers.iteritems():
    paper["avgRating"] =\
        sum(paper["ratings"]) * 1.0/len(paper["ratings"])

print "Constructing Industry Review Table"
industryReviewTable = []
for review in industryReviews:
    paper = papers[review["industryId"]]

    industryReviewTable.append({
        "paperIndustryId": review["industryId"],
        "reviewerEmail": review["email"],

        "rating": review["overallRating"],

        "devPaperMean": review["overallRating"] - paper["avgRating"],

        ###Review Stats
        "reviewLength": len(
            ("%s %s" % (
                review["comments"],
                review["privateComments"])).split()),

        "time": np.datetime64(review["date"]),
    })

DataFrame(industryReviewTable).to_pickle(
    "savedFrames/iteration5/industryReviewTable")
