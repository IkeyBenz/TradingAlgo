from data.binance_api import get_klines_df

d = get_klines_df(
    symbol='TRXUSDT',
    interval='2h',
    limit=1000
)

print(d.head())
