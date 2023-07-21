import os
import pandas as pd
import numpy as np
# from statsmodels.tsa.arima.model import ARIMA
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense

def count_sum(string):
    sum_days = [0,0,0,0,0,0]
    k = 0
    for i in range(1, len(df["일"])):
        if df["일"][i] != 0:
            k+=1
        else:
            sum_days[k] += df[string][i]
    return sum_days[1:]

def flatten_2d_list(input_list):
    return [item for sublist in input_list for item in sublist]

def create_lstm_input(data, time_steps, next_day_steps):
    X, y = [], []
    for i in range(0, len(data)-time_steps, time_steps):
        X.append(list(data[i:i+time_steps]))
        y.append(list(data[i+time_steps:i+time_steps+next_day_steps]))
    return np.array(X), np.array(y)

'''
def set_data():
    path = "./../2023"
    flist = os.listdir(path)
    datas = []
    for t in range(len(flist)):
        weeks = []
        flattens = []
        file_path = path + "/" + flist[t]
        df = pd.read_excel(file_path)
        for i in range(7,24):
            weeks.append(count_sum(df.columns[i]))
        for i in range(5):
            for j in range(len(weeks)):
                flattens.append(weeks[j][i])
        datas.append(flattens)

    data = {
        'Date': pd.date_range(start='2023-03-17', periods=80*17, freq='H'),  # 날짜 정보 (시작 날짜와 주기, n은 주차 수)
        'Hour': list(range(6, 23)) * 80,  # 시간 정보 (6시부터 22시까지)
        'Passengers': flatten_2d_list(datas),  # 해당 시간의 이용객 수
    }

    df = pd.DataFrame(data)
    return df
'''
def model_eval():
    df = pd.read_excel("./../output.xlsx")

    time_steps = 17  # 하루에 해당하는 시간대 수
    next_day_steps = 17  # 다음날 하루에 해당하는 시간대 수

    X, y = create_lstm_input(df['Passengers'], time_steps, next_day_steps)

    split_idx = int(len(X) * 0.9)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    model = Sequential()
    model.add(LSTM(64, input_shape=(time_steps, 1), return_sequences=True))
    model.add(LSTM(64))
    model.add(Dense(64))
    model.add(Dense(32))
    model.add(Dense(next_day_steps))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, epochs=50, batch_size=17)
    model.save("lstm_model")

    return X_test
    
def model_pred(data):
    loaded_model = load_model("lstm_model")
    y_pred = loaded_model.predict(data)
    return y_pred[0]