# Engine/strategy.py

import pandas as pd

class SmaCrossStrategy:
    def __init__(self, short_window=50, long_window=200):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, df):
        df = df.copy()
        df['SMA_50'] = df['Close'].rolling(window=self.short_window).mean()
        df['SMA_200'] = df['Close'].rolling(window=self.long_window).mean()

        # Add signal column
        df['Signal'] = 0
        df.loc[df['SMA_50'] > df['SMA_200'], 'Signal'] = 1
        df.loc[df['SMA_50'] < df['SMA_200'], 'Signal'] = -1

        return df
