from __future__ import division
import dill as pickle
import string
from math import log
import agregator
import csv
import math
from pprint import pprint as pp

def get_features(feat, Y):
    rows = agregator.DBnewsMarked()
    return [[i[feat], i[Y]] for i in rows]

def clean(sentanse):
    translator = str.maketrans("", "", string.punctuation)
    return sentanse.translate(translator)


class NaiveBayesClassifier:
    def __init__(self, alpha = 0.55):
        self.alpha = alpha

    def fit(self, X, y):
        classes, chances = {}, {}
        all_words = []
        labels = set(y)
        for sentence in X:
            for word in sentence.split():
                all_words.append(word)
                for label in labels:
                    classes[label] = 0
                    chances[(label, word)] = 0.55
        for sentence, label in zip(X, y):
            for word in sentence.split():
                classes[label] += 1
                chances[(label, word)] += 1
        length = len(set(all_words))
        for tuple, cnt in chances.items():
            chances[tuple] = cnt / (classes[tuple[0]] + length)
        argues = classes, chances
        return argues


    def predict(self, X_sentence, argues):
        pred = {}
        classes, prob = argues
        for key in classes.keys():
            pred[key] = 0
            for word in X_sentence.split():
                try:
                    pred[key] += math.log(prob[(key, word)])
                except:
                    pass
        final = []
        for label in pred.keys():
            final.append(pred[label])
        for label in pred.keys():
            if pred[label] == max(final):
                return label

    def score(self, X_test, y_test):
        score = 0
        for current_X, current_Y in zip(X_test, y_test):
            if (self.predict(current_X) == current_Y):
                score += 1
        score /= len(X_test)
        return score

if __name__ == '__main__':
    X, Y = [], []
    with open("SMSSpamCollection") as f:
        data = list(csv.reader(f, delimiter="\t"))
    for target, msg in data:
        X.append(msg)
        Y.append(target)

    # features = get_features('title', 'likes')
    # X = [i[0] for i in features]
    # Y = [i[1] for i in features]
    # print(len(X))
    # print(len(Y))

    X = [clean(x).lower() for x in X]
    X_test, Y_test, X_train, Y_train = X[3900:], Y[3900:], X[:3900], Y[:3900]

    model = NaiveBayesClassifier()
    model.fit(X_train, Y_train)
