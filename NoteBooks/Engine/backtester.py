# engine/backtester.py

# Engine/backtester.py

import pandas as pd

class BacktestEngine:
    def __init__(self, df, strategy, initial_cash=100000, slippage_pct=0.001, fee_per_trade=1.0, stop_loss_pct=None, take_profit_pct=None):
        self.df = df.copy()
        self.strategy = strategy
        self.initial_cash = initial_cash
        self.slippage_pct = slippage_pct
        self.fee_per_trade = fee_per_trade
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct


    def run(self):
        df = self.strategy.generate_signals(self.df)

        cash = self.initial_cash
        shares = 0
        portfolio_value = []

        fentry_price = None

        for i in range(len(df)):
            row = df.iloc[i]
            price = float(row['Close'])
            signal = int(row['Signal'])
            entry_price = None

            # --- Entry condition ---
            if signal == 1 and shares == 0:
                buy_price = price * (1 + self.slippage_pct)
                shares = cash // buy_price
                cash -= shares * buy_price + self.fee_per_trade
                entry_price = price

            # --- Exit condition (signal) ---
            elif signal == -1 and shares > 0:
                sell_price = price * (1 - self.slippage_pct)
                cash += shares * sell_price - self.fee_per_trade
                shares = 0
                entry_price = None

            # --- Exit condition (stop loss or take profit) ---
            elif shares > 0 and entry_price:
                if self.stop_loss_pct and price <= entry_price * (1 - self.stop_loss_pct):
                    # Stop loss triggered
                    sell_price = price * (1 - self.slippage_pct)
                    cash += shares * sell_price - self.fee_per_trade
                    shares = 0
                    entry_price = None

                elif self.take_profit_pct and price >= entry_price * (1 + self.take_profit_pct):
                    # Take profit triggered
                    sell_price = price * (1 - self.slippage_pct)
                    cash += shares * sell_price - self.fee_per_trade
                    shares = 0
                    entry_price = None

            portfolio_value.append(cash + shares * price)


        df['Portfolio Value'] = portfolio_value
        return df
