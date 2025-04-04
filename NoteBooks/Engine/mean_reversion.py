# Engine/mean_reversion.py

import pandas as pd
import numpy as np

class MeanReversionStrategy:
    def __init__(self, window=20, threshold=0.001):
        self.window = window
        self.threshold = threshold  # 3%

    def generate_signals(self, df):
        df = df.copy()
        # Calculate the moving average
        df['MA'] = df['Close'].rolling(window=self.window).mean()
        df['Signal'] = 0

        # Force the arrays to be 1-dimensional
        close_arr = df['Close'].to_numpy().ravel()
        ma_arr = df['MA'].to_numpy().ravel()

        # Now, perform element-wise comparisons
        condition_buy = pd.Series(
            close_arr < (1 - self.threshold) * ma_arr,
            index=df.index
        )
        condition_sell = pd.Series(
            close_arr > (1 + self.threshold) * ma_arr,
            index=df.index
        )

        df.loc[condition_buy, 'Signal'] = 1   # Buy signal
        df.loc[condition_sell, 'Signal'] = -1  # Sell signal

        return df
