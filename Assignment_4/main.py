
# Import the necessary modules and libraries
import numpy as np
import time

from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn import preprocessing



path = "C:\Users\yann\Documents\Mes fichiers\Cours\GeorgiaTech\Fall 2016\CS   8803 - Big Data Systems and Analytics\Assignments\Programming 4\Data\\"


""" Function to test one method of classification
Split first the data set to make a learning and a prediction
Then try a crossvalidation with 5 folds
Input:
    - ml: sklearn algorithm
    - X: np.matrix which contains features
    - y: vector of label
Output:
    - { 'name': String, 'scores': [1, ...], 'mean', 'std', 'score1', 'time' }
"""
def genericTest(ml, X, y):
    print ">>>>>>>>>>>>>>", ml.__class__.__name__
    start_time = time.clock()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
    ml.fit(X_train, y_train)
    score1 = ml.score(X_test, y_test)
    scores = cross_val_score(ml, X, y, cv=4)   # Scores computed cv=5 times
    print score1, scores, "\n"
    time_total = (time.clock() - start_time)
    return {'name': ml.__class__.__name__, 'scores': scores,
            'mean': scores.mean(), 'std': scores.std(),
            'score1': score1,
            'time': time_total}


""" Import a file
Input:
    - filename: String
    - nbLine: Int: Number of lines present on the file
    - nbCol: Int: Number of features contained on the file
Output:
    - np.chararray((nbLine, nbCol))
"""
def importFile(filename, nbLine, nbCol, separator=","):
    output = np.chararray((nbLine, nbCol))
    file = open(path + filename, 'r')
    i = 0
    for line in file.readlines():
        s = line.strip().split(separator)
        for e in range(0, nbCol):
            output[i, e] = s[e]
        i += 1
    file.close()
    return output


""" Save results on a file
Input:
    - filename: String
    - dico: [{ 'name': String, 'scores': [1, ...], 'mean', 'std', 'score1', 'time' }], ... ]List of data to save
Output:
    - None
"""
def saveResults(filename, dico):
    file = open(filename, 'w+')
    separator = ';'
    for line in dico:
        file.write(line['name'] + separator + separator.join([str(line['scores'][l]) for l in range(0, len(line['scores']))]) +
                   separator + str(line['mean']) + separator + str(line['std']) + separator + str(line['score1']) +
                   separator + str(line['time']) + '\n')
    file.close()


def GaussianTest(X, y):
    gnb = GaussianNB()
    y_pred = gnb.fit(X, y).predict(X)
    print("Number of mislabeled points out of a total %d points : %d"
      % (X.shape[0], (y != y_pred).sum()))
    scores = cross_val_score(gnb, X, y, cv=4)   # Scores computed cv=5 times
    print scores
    return gnb



if __name__ == '__main__':
    # Models
    dtr2 = DecisionTreeClassifier(max_depth=2)
    dtr5 = DecisionTreeClassifier(max_depth=5)
    gnb = GaussianNB()
    clf = svm.SVC(kernel='linear', C=1)
    clf_2 = svm.SVC()

    clf1 = LogisticRegression(random_state=1)
    clf2 = RandomForestClassifier(random_state=1)
    clf3 = GaussianNB()

    rfc_1 = RandomForestClassifier(random_state=1)


    list_ml = [dtr2, dtr5, gnb, clf, clf_2, clf1, clf2, clf3]


    # Dataset
    # ## First input data
    # filename = "agaricus-lepiota.data"
    # X = importFile(filename, 8124, 23)
    # le = preprocessing.LabelEncoder()   # Great the object to convert string to vector
    # X_ = np.zeros((8124, 23))
    # for col in range(0, 23):
    #     le.fit(np.transpose(X[:, col]))
    #     X_[:, col] = le.transform(X[:, col])
    # y = X_[:, 0]
    # X = X_[:, 1:]

    ## Second test
    filename = "glass.data"
    X = np.loadtxt(path + filename, delimiter=",")
    y = X[:, 10]
    X = X[:, 1:-1]


    listResults = []


    ## WeakLearner
    print '############### WeakLearner ###############'
    for ml in list_ml:
        listResults.append(genericTest(ml, X, y))


    ## Bagging
    print '############### Bagging ###############'
    bagging = BaggingClassifier(KNeighborsClassifier(), max_samples=0.5, max_features=0.5)
    listResults.append(genericTest(bagging, X, y))

    bagging = BaggingClassifier(LogisticRegression(), max_samples=0.5, max_features=0.5)
    listResults.append(genericTest(bagging, X, y))

    bagging = BaggingClassifier(DecisionTreeClassifier(max_depth=2), max_samples=0.5, max_features=0.5)
    listResults.append(genericTest(bagging, X, y))

    bagging = BaggingClassifier(GaussianNB(), max_samples=0.5, max_features=0.5)
    listResults.append(genericTest(bagging, X, y))

    bagging = BaggingClassifier(svm.SVC(), max_samples=0.5, max_features=0.5)
    listResults.append(genericTest(bagging, X, y))



    ## Boosting
    print '############### Boosting ###############'
    clf = AdaBoostClassifier(n_estimators=300)
    listResults.append(genericTest(clf, X, y))

    clf = ExtraTreesClassifier(n_estimators=300)
    listResults.append(genericTest(clf, X, y))

    clf = GradientBoostingClassifier(n_estimators=500, learning_rate=0.2, max_depth=1, random_state=0)
    listResults.append(genericTest(clf, X, y))

    clf = RandomForestClassifier(random_state=1)
    listResults.append(genericTest(clf, X, y))


    clf = VotingClassifier(estimators=[('dt', clf1), ('knn', clf2), ('svc', clf3)], voting='soft', weights=[2, 1, 2])
    listResults.append(genericTest(clf, X, y))

    clf = VotingClassifier(estimators=[('dt', clf1), ('knn', clf2), ('svc', clf3)], voting='hard', weights=[2, 1, 2])
    listResults.append(genericTest(clf, X, y))

    clf = VotingClassifier(estimators=[('dt', clf1), ('knn', clf2), ('svc', clf3)], voting='hard')
    listResults.append(genericTest(clf, X, y))


    ## Save results on a file
    saveResults(filename + '_results.csv', listResults)