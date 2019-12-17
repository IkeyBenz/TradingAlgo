"""
In order to train and test a model, we'll need some stock's data. This file uses the
py-pi package known as pandas_datareader to pull market data from the Quandl api.

To reduce redundant api calls, we store the raw data in data/raw/. Those dataframes
simply contain columns for 'high,low,open,close,volume'.
"""
import pandas as pd

from os import path, listdir

from .binance_api import get_klines_df
from .augment import with_inidicators
from .labler import with_labels

RAW_DATA_DIR = path.join('data', 'raw')
PROCESSED_DATA_DIR = path.join('data', 'processed')


def load_raw(symbol: str, update=False) -> pd.DataFrame:
    """
    #### Loads the data of a stock as it would be returned by Quandl
        :param symbol {str} The stock symbol whose data should be loaded
        :param update {bool} If True, will download new symbols data
        :return pd.DataFrame
    """

    file_path = path.join(RAW_DATA_DIR, f'{symbol}.csv')

    if update or not path.exists(file_path):
        file_path = _download_raw(symbol)

    return pd.read_csv(file_path)


def load_processed(symbol: str, update=False) -> pd.DataFrame:
    """
    ### Loads the dataframe of a given stock symbol including all TA features and buy/sell labels.
        :param symbol {str} The stock symbol whose data should be loaded
        :param update {bool} If True, will download new symbols data
        :return pd.DataFrame
    """
    file_path = path.join(PROCESSED_DATA_DIR, f'{symbol}.csv')

    if update or not path.exists(file_path):
        raw_df = load_raw(symbol, update)
        processed = with_inidicators(with_labels(raw_df)).dropna()
        processed.to_csv(file_path)

    return pd.read_csv(file_path)


def _download_raw(symbol: str):
    """
    ### Pulls symbol data from quandl and stores it in {RAW_DATA_PATH}/symbol.csv
        :param symbol {str} The stock symbol whose data we should dowload
        :return str The absolute file path of the downloaded dataframe.
    """
    file_path = path.join(RAW_DATA_DIR, f'{symbol}.csv')

    df = get_klines_df(symbol=symbol, limit=1000, interval='12h')
    df.to_csv(file_path)

    return file_path
