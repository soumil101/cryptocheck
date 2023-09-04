import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential

data = pd.read_csv('data/_test.csv')

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data['BTC'].values.reshape(-1, 1))

prediction_hours = 50

x_train, y_train = [], []

for x in range(prediction_hours, len(scaled_data)):
    x_train.append(scaled_data[x - prediction_hours:x, 0])
    y_train.append(scaled_data[x, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

model = Sequential()

model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
# model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
# model.add(Dropout(0.2))
model.add(LSTM(units=50))
# model.add(Dropout(0.2))
model.add(Dense(units=1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, epochs=25, batch_size=32)

test_data = pd.read_csv('data/_test2.csv')
actual_prices = test_data['BTC'].values

total_dataset = pd.concat((data['BTC'], test_data['BTC']), axis=0)

model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_hours:].values
model_inputs = model_inputs.reshape(-1, 1)
model_inputs = scaler.transform(model_inputs)

x_test = []

for x in range(prediction_hours, len(model_inputs)):
    x_test.append(model_inputs[x - prediction_hours:x, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

predicted_prices = model.predict(x_test)
predicted_prices = scaler.inverse_transform(predicted_prices)

plt.plot(actual_prices, color='black', label='Actual Prices')
plt.plot(predicted_prices, color='green', label='Predicted Prices')
plt.title('BTC Price Prediction')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend(loc='upper left')
plt.show()