"""
Every row of our stock symbol dataframes need to be labeled with the expected (buy, sell,
do nothing) action.

This file's with_labels function adds the expected actions for each row.
"""
import pandas as pd
import numpy as np


def with_labels(df: pd.DataFrame):
    in_position = False
    for i, row in df.iterrows():
        try:
            price_increase = df.loc[i, 'close'] < df.loc[i+1, 'close']
            if price_increase:
                df.loc[i, 'PREDICTION'] = 1
            else:
                df.loc[i, 'PREDICTION'] = -1
        except:
            pass

    return df
