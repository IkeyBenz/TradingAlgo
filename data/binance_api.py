import pandas as pd
from binance.client import Client

from os import getenv

client = Client(getenv('BINANCE_API_KEY'), getenv('BINANCE_SECRET_KEY'))


def get_klines_df(**params) -> pd.DataFrame:
    cols = [
        'opentime', 'open', 'high', 'low', 'close', 'volume',
    ]
    to_ignore = [
        'closetime', 'quote_asset_vol', 'num_trades', 'taker_buy_base_asset_vol',
        'taker_buy_quote_asset_volume', 'dont_even_know'
    ]
    data = client.get_klines(**params)
    df = pd.DataFrame(data, columns=[*cols, *to_ignore])
    return df.drop([*to_ignore, 'opentime'], axis=1)
