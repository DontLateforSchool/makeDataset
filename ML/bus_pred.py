import os
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
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

# LSTM 입력 데이터 생성
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
    df = pd.read_excel("./output.xlsx")

    time_steps = 17  # 하루에 해당하는 시간대 수
    next_day_steps = 17  # 다음날 하루에 해당하는 시간대 수

    # LSTM 입력 데이터 생성
    X, y = create_lstm_input(df['Passengers'], time_steps, next_day_steps)

    # 데이터를 학습용과 테스트용으로 분리
    split_idx = int(len(X) * 0.9)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]


    # LSTM 모델 생성과 학습
    model = Sequential()
    model.add(LSTM(64, input_shape=(time_steps, 1), return_sequences=True))  # return_sequences=True로 설정하여 다음 LSTM 레이어로 출력 전달
    model.add(LSTM(64))  # 두 번째 LSTM 레이어
    model.add(Dense(next_day_steps))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, epochs=100, batch_size=17)
    model.save("lstm_model")
    
def model_pred(data):
    loaded_model = load_model("lstm_model")
    y_pred = loaded_model.predict(data)
    return y_pred[0]