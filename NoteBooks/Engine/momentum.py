# Engine/momentum.py

import pandas as pd

class MomentumStrategy:
    def __init__(self, lookback=10, threshold=0.02):
        self.lookback = lookback
        self.threshold = threshold

    def generate_signals(self, df):
        df = df.copy()
        df['Returns'] = df['Close'].pct_change(self.lookback)
        df['Signal'] = 0
        df.loc[df['Returns'] > self.threshold, 'Signal'] = 1
        df.loc[df['Returns'] < -self.threshold, 'Signal'] = -1
        return df
