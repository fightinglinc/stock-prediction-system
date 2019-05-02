import pandas as pd




def ema(data, period=0, column='close'):
    data['ema' + str(period)] = data[column].ewm(ignore_na=False, min_periods=period, com=period, adjust=True).mean()

    return data

def macd(data, period_long=26, period_short=12, period_signal=9, column='close'):
    data = pd.DataFrame(data,columns=['close'])
    remove_cols = []
    if not 'ema' + str(period_long) in data.columns:
        data = ema(data, period_long)
        remove_cols.append('ema' + str(period_long))

    if not 'ema' + str(period_short) in data.columns:
        data = ema(data, period_short)
        remove_cols.append('ema' + str(period_short))

    data['macd_val'] = data['ema' + str(period_short)] - data['ema' + str(period_long)]
    data['macd_signal_line'] = data['macd_val'].ewm(ignore_na=False, min_periods=0, com=period_signal, adjust=True).mean()

    data = data.drop(remove_cols, axis=1)
    return data['macd_val'].values.tolist()

def rsi(data, periods=14, close_col='close'):
    data = pd.DataFrame(data,columns=['close'])
    data['rsi_u'] = 0.
    data['rsi_d'] = 0.
    data['rsi'] = 0.

    for index,row in data.iterrows():
        if index >= periods:

            prev_close = data.at[index-periods, close_col]
            if prev_close < row[close_col]:
                data.set_value(index, 'rsi_u', float(row[close_col]) - float(prev_close))
            elif prev_close > row[close_col]:
                data.set_value(index, 'rsi_d', float(prev_close) - float(row[close_col]))

    data['rsi'] = data['rsi_u'].ewm(ignore_na=False, min_periods=0, com=periods, adjust=True).mean() / (data['rsi_u'].ewm(ignore_na=False, min_periods=0, com=periods, adjust=True).mean() + data['rsi_d'].ewm(ignore_na=False, min_periods=0, com=periods, adjust=True).mean())

    data = data.drop(['rsi_u', 'rsi_d'], axis=1)

    return data['rsi'].values.tolist()



def moving_avg(data, period=50):
    data = pd.DataFrame(data,columns=['close'])
    data['moving'] = data['close'].rolling(period).mean()
    return data['moving'].values.tolist()
