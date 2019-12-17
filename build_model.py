'''
The plan here is to design an evolutionary stock trading algorithm.
Basically the idea is that if we have thousands of randomly generated "trading strategies,"
and test them all out in the stock market, we'll be able to see which strategies
worked the most, and so we can then redo the simulation but this time the trading strategies
will have adjusted according to the better performing ones. After many itterations of
this, the stategies autonymously evolve into their best possible forms.

In order to generate thousands of random trading strategies, each strategy will need
to have a decision tree that takes in many different indicators as input, and spits out
a buy or sell action. In order to make thousands of strategies using only tens of indicators,
each strategy will set different threshholds for each of their indicators (different values that
trigger them to say buy or sell), ensuring that every strategy is truely random.

To further optimize this approach, we should have it learn which indicators to prioritize.
Rather than using a decision tree to store our indicators, we will use a priority queue.
'''
import sklearn
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from graphviz import Source

from os import path
import pickle

from data import load_processed


def build_classifier_for(symbol: str) -> sklearn.tree.DecisionTreeClassifier:
    df = load_processed(symbol)
    X, y = df.drop('PREDICTION', axis=1), df[['PREDICTION']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False)
    clf = DecisionTreeClassifier().fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    return acc, clf


def save_best_model(symbol: str):
    clf_path = path.join('classifiers', f'{symbol}.pickle')
    graph_path = path.join('classifiers', f'{symbol}.dot')

    best_acc, best_clf = build_classifier_for(symbol)
    for _ in range(100):
        acc, clf = build_classifier_for(symbol)
        if acc > best_acc:
            best_acc, best_clf = acc, clf

    with open(graph_path, 'w') as dotfile:
        export_graphviz(best_clf, out_file=dotfile)

    with open(clf_path, 'wb') as clf_file:
        clf_file.write(pickle.dumps(clf))

    print(f"Saved classifier for {symbol} with accuracy of {best_acc}")
