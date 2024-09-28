import os
import sys
import json
import pandas as pd
import numpy as np

def get_returns(soxx):
    soxx['intraday_p_change'] = soxx.close - soxx.open
    soxx.loc[1:,'day_p_change'] = soxx.close - soxx.close.shift(1)
    soxx.loc[1:,'day_return'] = (soxx.day_p_change / soxx.close.shift(1))

    # Add a 'total_return' column which is the cumulative product of (1 + day_return)
    soxx['total_return'] = (1 + soxx['day_return']).cumprod()

    # Calculate moving averages for 9, 50, 90, and 200 days
    #soxx['sma_9'] = soxx['close'].rolling(window=9).mean()
    #soxx['sma_50'] = soxx['close'].rolling(window=50).mean()
    #soxx['sma_90'] = soxx['close'].rolling(window=90).mean()
    #soxx['sma_200'] = soxx['close'].rolling(window=200).mean()

    # Calculate exponential moving averages (EMAs) with smoothing factor of 2
    period_size = 3
    soxx['ema_50'] = soxx['close'].ewm(span=50*period_size, adjust=False).mean()
    soxx['ema_90'] = soxx['close'].ewm(span=90*period_size, adjust=False).mean()
    soxx['ema_200'] = soxx['close'].ewm(span=200*period_size, adjust=False).mean()

    # Calculate the macd
    soxx['macd'] = soxx.ema_50 - soxx.ema_90

    # Calculate the signal
    soxx['signal'] = soxx['macd'].ewm(span=9*0.5*period_size, adjust=False).mean()

    soxx['trigger'] = (soxx['macd'] < soxx['signal']).astype(int)

    # add a day return for strategy_1: go to cash when macd crosses below its 9 period moving average
    soxx['strategy_1_day_return'] = (1 - soxx.trigger)*soxx.day_return
    soxx['strategy_1_total_return'] = (1 + soxx['strategy_1_day_return']).cumprod()

    return soxx

