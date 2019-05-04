import pandas as pd
import csv
import numpy as np
from sklearn.svm import SVR


def get_raw_data(company_name):
    path = 'data/predict_data/'
    csv_file = path + company_name + '.csv'
    stocks = []
    with open(csv_file) as file:
        reader = csv.reader(file)
        for row in reader:
            stocks.append(row)

    df = pd.DataFrame(stocks[1:], columns=stocks[0]).iloc[::-1]
    df['close'] = df['close'].astype('float64')
    return df


def ema(data, period=0, column='close'):
    data['ema' + str(period)] = data[column].ewm(ignore_na=False, min_periods=period, com=period, adjust=True).mean()
    return data


def macd(data, period_long=26, period_short=12, period_signal=9, column='close'):
    remove_cols = []
    if not 'ema' + str(period_long) in data.columns:
        data = ema(data, period_long)
        remove_cols.append('ema' + str(period_long))

    if not 'ema' + str(period_short) in data.columns:
        data = ema(data, period_short)
        remove_cols.append('ema' + str(period_short))

    data['macd_val'] = data['ema' + str(period_short)] - data['ema' + str(period_long)]
    data['macd_signal_line'] = data['macd_val'].ewm(ignore_na=False, min_periods=0, com=period_signal,
                                                    adjust=True).mean()

    data = data.drop(remove_cols, axis=1)

    return data


def rsi(data, periods=14, close_col='close'):
    data['rsi_u'] = 0.
    data['rsi_d'] = 0.
    data['rsi'] = 0.
    for index, row in data.iterrows():
        if index >= periods:

            prev_close = data.at[index - periods, close_col]
            if prev_close < row[close_col]:
                data.at[index, 'rsi_u'] = float(row[close_col]) - float(prev_close)
            elif prev_close > row[close_col]:
                data.at[index, 'rsi_d'] = float(prev_close) - float(row[close_col])

    data['rsi'] = data['rsi_u'].ewm(ignore_na=False, min_periods=0, com=periods, adjust=True).mean() / (
            data['rsi_u'].ewm(ignore_na=False, min_periods=0, com=periods, adjust=True).mean() + data['rsi_d'].ewm(
        ignore_na=False, min_periods=0, com=periods, adjust=True).mean())

    data = data.drop(['rsi_u', 'rsi_d'], axis=1)
    return data


def get_features(data, is_long_term):
    # predict next long_term_day
    long_term_day = 30
    Next = None
    if is_long_term is True:
        data['moving_50'] = data['close'].rolling(50).mean()  # Calculate Moving Average 50
        data['moving_100'] = data['close'].rolling(100).mean()  # Calculate Moving Average 100
        Next = data['close'][100 + long_term_day:].copy()
        data = data[99:-long_term_day][['close', 'moving_50', 'moving_100']].copy()  # Choose 3 columns
    else:
        data = macd(data)  # Calculate MACD
        data = rsi(data)  # Calculate RSI
        # 25 is to get rid of NaN
        macd_start = 25
        # +1 is for next day
        Next = data['close'][macd_start + 1:].copy()
        data = data[macd_start:][['close', 'rsi', 'macd_val']].copy()  # Choose 3 columns
    Next = Next.reset_index(drop=True)
    data = data.reset_index(drop=True)
    data['next'] = Next
    return data


def get_train_data(data_with_feature):
    return data_with_feature[:161, :3], data_with_feature[:161, 3]


def get_test_data(data_with_feature):
    return data_with_feature[161:-1, :3], data_with_feature[161:-1, 3]


def get_predict_data(data_with_feature):
    return data_with_feature[-1, :3].reshape((1, 3))


def build_SVM_model():
    clf = SVR(gamma='scale', C=1.0, epsilon=0.2)
    return clf


def rmse(predict, truth):
    return np.sqrt(np.mean((predict - truth) ** 2))


def train_SVM_model(clf, train_data, target_data):
    clf.fit(train_data, target_data)


def test_SVM_model(clf, test_data, truth_data):
    predict_test = clf.predict(test_data)
    return rmse(predict_test, truth_data)


def predict_SVM_model(clf, predict_data):
    return clf.predict(predict_data)


def get_next_day_price(company_name, is_long_term=False):
    pd_raw = get_raw_data(company_name)
    pd_with_feature = get_features(pd_raw, is_long_term)
    np_data = pd_with_feature.to_numpy()
    np_train, np_target = get_train_data(np_data)
    np_test, np_truth = get_test_data(np_data)
    np_pred = get_predict_data(np_data)
    svm = build_SVM_model()
    train_SVM_model(svm, np_train, np_target)
    # print(test_SVM_model(svm, np_test, np_truth))
    return predict_SVM_model(svm, np_pred)
