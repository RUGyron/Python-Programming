from __future__ import division
import csv
import string
from collections import defaultdict
from math import log
from agregator import DBnews, DBnewsMarked
from pprint import pprint as pp


class NaiveBayesClassifier:
    def __init__(self, alpha = 1):
        self.alpha = alpha

    def fit(self, X, y):
        classes, freq = defaultdict(lambda: 0), defaultdict(lambda: 0)
        for feats, label in zip(X, y):
            classes[label] += 1  # count classes frequencies
            for feat in str(feats).split(): # str(feats) instead of feats !!!
                freq[label, feat] += 1  # count features frequencies

        for label, feat in freq:  # normalize features frequencies
            freq[label, feat] /= classes[label]
        for c in classes:  # normalize classes frequencies
            classes[c] /= len(y)
        self.classifier = classes, freq  # return P(C) and P(O|C)

    def predict(self, X):
        classes, prob = self.classifier
        return min(classes.keys(),  # calculate argmin(-log(C|O))
                   key=lambda cl: -log(classes[cl]) + \
                                  sum(-log(prob.get((cl, feat), 10 ** (-7))) for feat in str(X))) # str(X) instead of X !!!

    def score(self, X_test, y_test):
        score = 0
        for current_X, current_Y in zip(X_test, y_test):
            if (self.predict(current_X) == current_Y):
                score += 1
        score /= len(X_test)
        return score


def get_features():
    rows = DBnewsMarked()
    features = [[i['likes'], i['label']] for i in rows]
    return features

def clean(sentanse):
    translator = str.maketrans("", "", string.punctuation)
    return sentanse.translate(translator)

if __name__ == '__main__':
    features = get_features()
    X = [i[0] for i in features]
    Y = [i[1] for i in features]

    # X, Y = [], []
    # with open("SMSSpamCollection") as f:
    #     data = list(csv.reader(f, delimiter="\t"))
    # for target, msg in data:
    #     X.append(msg)
    #     Y.append(target)
    #
    # X = [clean(x).lower() for x in X]

    X_train, Y_train, X_test, Y_test = X[:500], Y[:500], X[500:], Y[500:]

    model = NaiveBayesClassifier()
    model.fit(X_train, Y_train)

    # print(model.score(X_test, Y_test))
