import sklearn
from sklearn.model_selection import train_test_split
import pickle

from os import path
from sys import argv
from time import sleep

from build_model import save_best_model
from data.load import load_processed


def load_model(symbol: str, update=False) -> sklearn.tree.DecisionTreeClassifier:
    model_path = path.join('classifiers', f'{symbol}.pickle')
    if update or not path.exists(model_path):
        save_best_model(symbol)
    return pickle.load(open(model_path, 'rb'))


def simulate_profits_for(df, clf, X_test, position_percent=10):
    cash = 1000
    stock = 0

    predictions = clf.predict(X_test)
    for curr_price, prediction in zip(X_test['close'], predictions):
        if prediction == 1:  # We should buy
            investment = cash / position_percent
            cash -= investment
            stock += investment / curr_price
            print(
                f"BUYING {investment / curr_price} for {investment}. Cash: {cash} | Stock: {stock}")
        else:  # We should sell
            withdrawal = stock / position_percent
            stock -= withdrawal
            cash += withdrawal * curr_price
            print(
                f"SELLING {withdrawal * curr_price} for {withdrawal}. Cash: {cash} | Stock: {stock}")
        sleep(0.1)

    print('Number of trades:', len(predictions))
    print(cash, stock, 'portfolio value:', cash + stock*curr_price)

    return cash + stock*curr_price


def find_best_position_percent(df, clf, X_test):
    optimal_percent = 1
    largest_gains = float('-inf')
    for percent in range(1, 101):
        profit = simulate_profits_for(df, clf, X_test, percent)
        print(f'Profit when trading at {percent}%: {profit}')
        if profit > largest_gains:
            largest_gains = profit
            optimal_percent = percent
    return optimal_percent, largest_gains


if __name__ == '__main__':
    symbol = argv[1]
    df = load_processed(symbol)
    clf = load_model(symbol, update=True)
    X_test = df[int(len(df)*0.75):].drop('PREDICTION', axis=1)
    resulting_portfolio = simulate_profits_for(df, clf, X_test)
    print(resulting_portfolio)
