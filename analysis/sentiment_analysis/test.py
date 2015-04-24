import re
import random
from feature_extraction.dataLoader import DataLoader
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
from sets import Set
import numpy as np
from utilities import Stemmer
from utilities.corenlp import StanfordCoreNLP
from utilities import pexpect


stemmer = Stemmer.Stemmer("english")

def getFeatures(text):
    #words = stemmer.stemWords(
    #    re.sub('[^\w\s]', ' ', text).lower().split())

    words = re.sub('[^\w\s]', ' ', text).lower().split()

    return dict(
        [word, True] for word in words)


loader = DataLoader()
loader.loadUsers()
loader.loadPapers()
loader.loadReviews()

# dataSet = []

# totalPositive = 0.0
# totalNegative = 0.0
# totalNeutral = 0.0

# for id, review in loader.reviews.iteritems():
#     if np.abs(review.overallRating) > 1:
#         ratings = review.ratings
#         reviewText = "%s %s %s" % (
#             ratings["strengths"],
#             ratings["weaknesses"],
#             ratings["comments"])

#         isPostive = review.overallRating > 0

#         if review.overallRating >= 2:
#             sentiment = "positive"
#             totalPositive += 1
#         elif review.overallRating <= -2:
#             sentiment = "negative"
#             totalNegative += 1
#         else:
#             sentiment = "neutral"
#             totalNeutral += 1

#         print reviewText

#         dataSet.append((getFeatures(reviewText), sentiment))

# samples = len(dataSet)

# accuracies = []

# for j in range(1):
#     random.shuffle(dataSet)
#     for i in range(10):
#         trainSet =\
#             dataSet[:(samples*i)/10] + dataSet[(samples*(i+1))/10:]
#         testSet = dataSet[(samples*i)/10:(samples*(i+1))/10]

#         classifier = NaiveBayesClassifier.train(trainSet)
#         accuracies.append(accuracy(classifier, testSet))

# print "CV-Accuracy: %f" % np.average(accuracies)
# print "CV-STDDEV: %f" % np.std(accuracies)
# print "Proportion of Negative Samples: %f" % (totalNegative/samples)
# print "Proportion of Positive Samples: %f" % (totalPositive/samples)

# classifier = NaiveBayesClassifier.train(dataSet)
# classifier.show_most_informative_features(5)

scoreDict = {
    "Neutral": 0,
    "Negative": -1,
    "Very negative": -2,
    "Positive": 1,
    "Very positive": 2
}


def processText(text, annotator):
    text = re.sub('[^\w\s\.]', ' ', text)
    text = re.sub(' +', ' ', text)
    sentences = re.sub('\.[^ ]', ';', text).split('.')

    score = 0

    for sentence in sentences:
        if len(sentence) > 5:
            print "SENDING LINE"
            annotator.sendline(sentence+"\n")
            annotator.expect("\r\n")
            print annotator.before
            annotator.expect("\r\n")
            print annotator.before
            while annotator.before[2:] not in scoreDict:
                annotator.expect("\r\n")
                print annotator.before
                print "Sentence is: %s" % sentence
            score += scoreDict[annotator.before[2:]]

    return score

print "Starting"

command = 'java -cp "./utilities/stanford-corenlp-full-2014-06-16/*"'\
          + ' -mx5g edu.stanford.nlp.sentiment.SentimentPipeline -stdin'
annotator = pexpect.spawn(command, maxread=8192, searchwindowsize=80)
annotator.expect("Processing will end when EOF is reached.\r\n")

truePositive = 0.0
falsePositive = 0.0
falseNegative = 0.0
trueNegative = 0.0
total = 0

print "There are %d total reviews" % len(loader.reviews)
for id, review in loader.reviews.iteritems():
    if np.abs(review.overallRating) > 1:
        if total >= 137:
            ratings = review.ratings

            totalScore = 0
            totalScore += processText(ratings["strengths"], annotator)
            totalScore += processText(ratings["weaknesses"], annotator)
            totalScore += processText(ratings["comments"], annotator)

            scorePos = totalScore > 0
            isPos = review.overallRating > 0

            if scorePos and isPos:
                truePositive += 1
            elif scorePos and not isPos:
                falsePositive += 1
            elif not scorePos and isPos:
                falseNegative += 1
            else:
                trueNegative += 1

                #print totalScore

        total += 1

        if total % 1 == 0:
            print total

print "Accuracy: %f" % ((truePositive + trueNegative)/total)
print "Correctly Classified Positives: %f" % (
    truePositive/(truePositive + falseNegative))
print "Correctly Classified Negatives: %f" % (
    trueNegative/(trueNegative + falsePositive))
