import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.models import load_model
import os

# Load user-uploaded CSV file
# Ensure the CSV file has headers: Date, Open, High, Low, Close
# file_path = r"StockAnalysis\Prediction\Data\HDFCBANK.csv"
file_path = r"B_stockAnalysis\Prediction\Data\ALLHDFCBANK.csv"

df = pd.read_csv(file_path)

# View the first few rows of the DataFrame
print(df.head())

# Explicitly specify date format
# df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y') #BankNifty
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d') #HDFCBANK


plt.plot(df['Close'])
plt.title('Stock Closing Price')
plt.xlabel('Date')
plt.ylabel('Price')

df = df[['Date', 'Close']]  # Keeping only 'Date' and 'Close' columns

dataset_train = df.iloc[:int(df.shape[0]*0.8), 1:2].values
dataset_test = df.iloc[int(df.shape[0]*0.8)-50:, 1:2].values  # Adjusted start index for test data

scaler = MinMaxScaler(feature_range=(-1, 1))
dataset_train = scaler.fit_transform(dataset_train)
dataset_test = scaler.transform(dataset_test)

def create_dataset(df, is_test=False):
    x = []
    y = []
    start = 100 if is_test else 0  # Adjust the start index
    end = df.shape[0] if is_test else df.shape[0]-100  # Adjust the end index
    
    for i in range(start, end):
        x.append(df[i-100:i, 0])  # Adjust the sequence length
        y.append(df[i, 0])
    
    x = [seq for seq in x if len(seq) == 100]
    y = y[len(y)-len(x):]
    
    x = np.array(x)
    y = np.array(y)
    return x, y


x_train, y_train = create_dataset(dataset_train)
x_test, y_test = create_dataset(dataset_test, is_test=True)

x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

model = Sequential()
model.add(LSTM(units=128, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=128, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=128, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=128))
model.add(Dropout(0.2))
model.add(Dense(units=1))


model.compile(loss='mean_squared_error', optimizer='rmsprop')


TrainedModel=r'B_stockAnalysis\Prediction\BF_closing_prediction_model1.h5'
if os.path.exists(TrainedModel):
    model = load_model(TrainedModel)
else:
    model.fit(x_train, y_train, epochs=100, batch_size=32)
    model.save('B_stockAnalysis\Prediction\BF_closing_prediction_model1.h5')

predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)
y_test_scaled = scaler.inverse_transform(y_test.reshape(-1, 1))

fig, ax = plt.subplots(figsize=(16,8))
ax.set_facecolor('black')
ax.plot(y_test_scaled, color='red', label='Original price')
plt.plot(predictions, color='cyan', label='Predicted price')
plt.title('Stock price vs Predict price')
plt.legend()

# Define a function to generate future dates
def generate_future_dates(start_date, num_days):
    date_range = pd.date_range(start=start_date, periods=num_days, freq='B')
    return date_range

# Modify the generate_future_data function to print predicted values
def generate_future_data(model, scaler, x_test, num_days):
    last_known_price = df['Close'].iloc[-1]
    future_dates = generate_future_dates(df['Date'].iloc[-1], num_days)
    
    # Use the last 50 data points to start generating future data
    input_data = x_test[-1,:,:].reshape(1, 100, 1)
    
    future_data = []

    for _ in range(num_days):
        prediction = model.predict(input_data)
        input_data = np.roll(input_data, -1)  # Shift data one step forward
        input_data[0,-1,0] = prediction[0,0]  # Append the prediction
        future_data.append(prediction[0,0])
    
    # Scale back the future data
    future_data = scaler.inverse_transform(np.array(future_data).reshape(-1, 1))
    
    # Print the predicted values in the terminal
    for date, price in zip(future_dates, future_data.ravel()):
        print(f"Date: {date}, Predicted Price: {price:.2f}")
    
    # Create a DataFrame for the future dates and predicted prices
    future_df = pd.DataFrame({'Date': future_dates, 'Close': future_data.ravel()})
    
    return future_df

# Generate and append future data
num_days = 30  # Define how many days into the future you want to predict
future_df = generate_future_data(model, scaler, x_test, num_days)
df_extended = pd.concat([df, future_df], ignore_index=True)

# Plot the extended data with labels
plt.figure(figsize=(16,8))
plt.plot(df_extended['Date'], df_extended['Close'], label='Historical Data')
plt.scatter(df_extended[-num_days:]['Date'], df_extended[-num_days:]['Close'], color='red', label='Predicted Prices')
plt.title('Stock Closing Price')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()