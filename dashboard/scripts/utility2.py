import pandas as pd
import numpy as np
from dashboard.scripts.utility import check_data_format

def add_return(df, period, percent=False):
    check_data_format(df)
    if percent:
        coeff = 100
    else:
        coeff = 1
    
    df['return'] = \
        coeff*(df['close'].shift(-1*period).divide(df['close']))-coeff
    return    

def add_SMA(df, period):
    check_data_format(df)
    df['SMA'] = \
        df['close'].rolling(window=period).mean()
    return

def add_SMA_deviation(df, period, percent=False):
    if 'SMA' not in df.columns:
        add_SMA(df, period)
    df['SMA_deviation'] = df['close'].sub(df['SMA'])
    if percent:
        df['SMA_deviation'] = 100*df['SMA_deviation'].divide(df['SMA'])
    return