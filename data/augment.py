"""
Financial Analysts often augment the standard dataframe of 'high,low,open,close,volume'
with many other indicators (RSI, MACD, EMA, SMA ... etc) when considering whether to buy
or sell. 

In order to augment our dataframes to include such indicators, we use the py-pi
package known as ta (stands for Technical Analysis).
"""
import pandas as pd
import ta


def with_inidicators(df):
    df = ta.add_all_ta_features(
        df, open='open', close='close', low='low', high='high', volume='volume')

    return df.drop(['trend_psar_up', 'trend_psar_down'], axis=1)
