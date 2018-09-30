import pandas as pd
import numpy as np
import random
from dashboard.scripts.security import Security
from bokeh.palettes import viridis

def check_data_format(df):
    cols = df.columns
    if 'open' not in cols:
        raise KeyError('\'open\' column missing.')
    if 'high' not in cols:
        raise KeyError('\'high\' column missing.')
    if 'low' not in cols:
        raise KeyError('\'low\' column missing.')
    if 'close' not in cols:
        raise KeyError('\'close\' column missing.')

def calculate_percent_return(prices, period):
    returns = 100*(prices.shift(-1*period)/prices)-100
    return returns

# def digitize2quantiles(series, num_quantiles):
#     labels = [str(i) for i in range(num_quantiles, 0, -1)]
#     quantiles = np.quantile(series.dropna(),)

def digitize2quartiles(series):
    labels = ['100%', '75%', '50%', '25%']
    quartiles = np.quantile(series.dropna(), [0.25, 0.5, 0.75, 1])

    def get_quartile(val):
        quartile = np.NaN
        for i, q in enumerate(sorted(quartiles, reverse=True)):
            if val <= q:
                quartile = labels[i]
            
        return quartile
    
    series_quartiles = series.apply(lambda x: get_quartile(x))

    return series_quartiles

def digitize2deciles(series):
    labels = ['{:d}0%'.format(i) for i in range(10, 0, -1)]
    percentiles = np.percentile(series.dropna(), [int(i) for i in range(10, 110, 10)])

    def get_decile(val):
        percentile = np.NaN
        for i, q in enumerate(sorted(percentiles, reverse=True)):
            if val <= q:
                percentile = labels[i]
        return percentile
    
    series_percentile = series.apply(lambda x: get_decile(x))

    return series_percentile

def digitize2sigma(series):
    mean = series.dropna().mean()
    std = series.dropna().std()
    
    def get_sigma(value):
        value_sigma = (value - mean)/std
        return value_sigma
    
    series_sigma = series.apply(lambda x: get_sigma(x))

    return series_sigma

def create_test_data(data):
    print('Setting up a security object...')
    security = Security(data)

    print('Adding MACD...')
    security.add_MACD(period_short=12, period_long=26, period_ave=9)
    print('  Adding MACD quartiles...')
    security.data['MACD_Quartile'] = \
                        digitize2quartiles(security.data['MACD'])
    print('  Adding MACD Decile...')
    security.data['MACD_Decile'] = \
                        digitize2deciles(security.data['MACD'])
    print('  Adding MACD signal quartiles...')
    security.data['MACD_signal_Quartile'] = \
                        digitize2quartiles(security.data['MACD_signal'])
    print('  Adding MACD signal Decile...')
    security.data['MACD_signal_Decile'] = \
                        digitize2deciles(security.data['MACD_signal'])
    
    print('Adding RSI...')
    security.add_RSI(rsi_period=14)
    print('  Adding RSI quartiles...')
    security.data['RSI_Quartile'] = digitize2quartiles(security.data['RSI'])
    print('  Adding RSI Decile...')
    security.data['RSI_Decile'] = digitize2deciles(security.data['RSI'])

    print('Adding Bollinger Bands...')
    security.add_BollingerBands(bollinger_period=20)
    
    print('Adding Deviation Metrics...')
    security.add_BollingeDeviations(bollinger_period=20)

    return security.data

def create_random_quartile(length):
    choices = [
        '1st-quartile', 
        '2nd-quartile', '2nd-quartile',
        '3rd-quartile', '3rd-quartile','3rd-quartile',
        '4th-quartile','4th-quartile','4th-quartile','4th-quartile']
    quartiles = [random.choice(choices) for _ in range(length)]
    return pd.Series(quartiles)




class Slice:
    def __init__(self, df, value_slice={}, range_slice={}):

        # Slice by values
        for key, value in value_slice.items():
            df = df[df[key] == value]

        # Slice by range
        for key, value in range_slice.items():
            if value[0] >= value[1]:
                raise ValueError("ERROR: 1st element in range must be smaller than the 2nd element.")
                #return    #This part should actually raise Exception to terminate
            df = df[(df[key] >= value[0]) & (df[key] <= value[1])]

        self.slice = df





if __name__ == '__main__':

    test_array = [1, 1, 2, 3, 4, 5, 6,7, 7, 8, 9, 10]
    test_array = np.array(test_array)
    print(np.quantile(test_array, [0.25, 0.5, 0.75, 1]))




### END ###