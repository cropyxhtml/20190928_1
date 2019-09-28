import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.tseries.offsets import MonthEnd
from sklearn.preprocessing import MinMaxScaler
df = pd.read_csv('./data/cansim-0800020-eng-6674700030567901031.csv',skiprows=6,
                 skipfooter=9, engine='python')
# print(df.head())
df['Adjustments'] = pd.to_datetime(df['Adjustments']) + MonthEnd(1)
df = df.set_index('Adjustments')
# print(df.head())
plt.plot(df)
plt.show()
split_date = pd.Timestamp('01-01-2011')
train = df.loc[:split_date,['Unadjusted']]
test = df.loc[split_date:,['Unadjusted']]
# ax = plt.plot(train)
plt.plot(test)# ax=ax)
plt.legend(['train','test'])
plt.show()
sc = MinMaxScaler()
train_sc = sc.fit_transform(train)
test_sc = sc.transform(test)
train_sc_df = pd.DataFrame(train_sc, columns=['Scaled'],index=train.index)
test_sc_df = pd.DataFrame(test_sc, columns=['Scaled'],index=test.index)
# print(train_sc_df.head())
'''
pondas shift 을 통해 window 만들기
shift는 이전 정보를 다음 row에서 다시쓰기 위한 pandas 함수
과거의 값을 총 12개로 저장하며, timestep 은 12개가 된다.
이 작업의 이유는 과거값 shift 1 ~ 12 를 통해 현재값 Scaled 을 예측하는 것
'''
for s in range(1,13):
    train_sc_df['shift_{}'.format(s)] = train_sc_df['Scaled'].shift(s)
    test_sc_df['shift_{}'.format(s)] = test_sc_df['Scaled'].shift(s)
# print(train_sc_df.head(13))
X_train = train_sc_df.dropna().drop('Scaled',axis=1)
y_train = train_sc_df.dropna()[['Scaled']]
X_test = train_sc_df.dropna().drop('Scaled',axis=1)
y_test = train_sc_df.dropna()[['Scaled']]
# 치종 트레이너 Set
print(X_train.head())
print(y_train.head())
#ndarray 로 변환
X_train = X_train.values
X_test = X_test.values
y_train = y_train.values
y_test = y_test.values
print(X_train.shape)
print(y_train.shape)
print(X_train)
print(y_train)
print('************')
X_train_t = X_train.reshape(X_train.shape[0],12,1)
X_test_t = X_test.reshape(X_test.shape[0],12,1)
print('최종 Data Set')
print(X_train.shape)
print(X_train)
print(y_train.shape)

#LSTM 모델 만들기
from keras.layers import LSTM,Dense
from keras.models import Sequential
from keras import backend as K
from keras.callbacks import EarlyStopping

K.clear_session()
model = Sequential()
model.add(LSTM(20, input_shape=(12,1))) # (timestamp, feature)
model.add(Dense(1)) # output = 1
model.compile(loss='mean_squared_error',optimizer='adam')
print(model.summary())

early_stop = EarlyStopping(monitor='loss', patience=1,verbose=1)
model.fit(X_train_t, y_train,30,100,1,callbacks=[early_stop],)
print('********** X_test_t **********')
print(X_test_t)
print('********** 모델 예측 predict 값 **********')
y_pred = model.predict(X_test_t)
print(y_pred)