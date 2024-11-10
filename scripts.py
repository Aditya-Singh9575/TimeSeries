# pip install yfinance (run the line if you have not installed yfinance)

#--------Scraping data----------

import yfinance as yf
symbol = "EURINR=X"
start_date = "2023-01-01"
end_date = "2024-10-01"  # setting end date to "2024-10-01" because there is not any data for 28 and 29th october
#download the data 
data = yf.download(symbol , start=start_date , end=end_date)
#saving data to a .csv file 
data.to_csv("EURINR_data.csv")  

#---------Technical analysis--------------

#data preprocessing
import pandas as pd
EURINR_data = pd.read_csv("EURINR_data.csv", header=[0, 1,2])
EURINR_data.columns = ['_'.join(col).strip() for col in EURINR_data.columns]  #flattening the multiindexed columns
EURINR_data.columns = ['Date', 'Adj Close','Close','High','Low','Open','Volume']  #renaming the columns
EURINR_data['Date'] = pd.to_datetime(EURINR_data['Date'])
EURINR_data.set_index("Date",inplace = True )  #setting 'Date' column as index

#----------1.SIMPLE MOVING AVERAGE------------ 
#(daily timeframe)
EURINR_data['SMA_20'] = EURINR_data['Close'].rolling(window=20, min_periods = 14, center=False).mean()

#SMA (weekly time frame)
weekly_data = EURINR_data['Close'].resample('W-MON').mean()  
SMA_4W = weekly_data.rolling(window=4, center=False).mean()
EURINR_data['SMA_4W'] = SMA_4W
EURINR_data['SMA_4W'].fillna(method='bfill',inplace=True)  #handling null values

#-----------2.BOLLINGER BAND--------------
#daily timeframe
std_20 = EURINR_data['Close'].rolling(window=20).std()  #Standard deviation in specified window size
EURINR_data['LowerBand'] = EURINR_data['SMA_20']-(2*std_20)   #Lower band
EURINR_data['UpperBand'] = EURINR_data['SMA_20']+(2*std_20)   #Upper band

#weekly timeframe
weekly_data = data['Close'].resample('W-MON').mean()
# Calculate the 20-week SMA
SMA_20W = weekly_data.rolling(window=20).mean()
# Calculate the 20-week standard deviation
STD_20W = weekly_data.rolling(window=20).std()
# Calculate the Upper and Lower Bollinger Bands
Upper_Band_W = SMA_20W + (2 * STD_20W)
Lower_Band_W = SMA_20W - (2 * STD_20W)
#column creation
EURINR_data['Upper_Band_W'] = Upper_Band_W
EURINR_data['Lower_Band_W'] = Lower_Band_W
#handling null values
EURINR_data['Upper_Band_W'].fillna(method='bfill',inplace=True)
EURINR_data['Lower_Band_W'].fillna(method='bfill',inplace=True)

#----------3.CCI (Commodity Channel Index)-------------
#daily timeframe

# Typical Price
typical_price = (EURINR_data['High'] + EURINR_data['Low'] + EURINR_data['Close']) / 3
# Simple Moving Average of Typical Price
sma_tp = typical_price.rolling(window=20).mean()
# Mean Deviation
def mean_absolute_deviation(x):
    return (x - x.mean()).abs().mean()

mean_deviation = typical_price.rolling(window=20).apply(mean_absolute_deviation, raw=False)
EURINR_data['cci'] = (typical_price - sma_tp) / (0.015 * mean_deviation)

#weekly timeframe

weekly_data = EURINR_data.resample('W-MON').agg({'High': 'max', 'Low': 'min', 'Close': 'last'})
# Typical Price
typical_price = (weekly_data['High'] + weekly_data['Low'] + weekly_data['Close']) / 3
# Simple Moving Average of Typical Price
sma_tp = typical_price.rolling(window=4).mean()
# Mean Deviation
def mean_absolute_deviation(x):
    return (x - x.mean()).abs().mean()

mean_deviation = typical_price.rolling(window=4).apply(mean_absolute_deviation, raw=False)
EURINR_data['cci_W'] = (typical_price - sma_tp) / (0.015 * mean_deviation)
EURINR_data['cci_W'].fillna(method = 'bfill',inplace=True)

#---------------------------technical analysis completed---------------------------------

clean_EURINR_data = EURINR_data.dropna()  #dropping rows having null values

#--------------------Decision Making---------------------------
#for single day time frame
def decision_1D(data):
    if (data['Close']<data['LowerBand']) and data['cci']<-100):
        print('BUY')
    elif (data['Close']>data['UpperBand']) and data['cci']>100):
        print('SELL')
    else:
        print('NEUTRAL')

#for weekly time frame
def decision_1W(data):
    if (data['Close']<data['Lower_Band_W']) and data['cci_W']<-100) :
        print('BUY')
    elif (data['Close']>data['Upper_Band_W']) and data['cci_W']>100) :
        print('SELL')
    else:
        print('NEUTRAL')


#example 
data = clean_EURINR_data.loc['2024-09-30']
decision_1D(data) # gave 'NEUTRAL' as output on the basis of  decision_1D function
decision_1W(data)  #gave 'NEUTRAL' as output on the basis of decision_1W function