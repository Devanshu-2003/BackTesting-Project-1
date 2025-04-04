# main.py

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from Engine.backtester import BacktestEngine


strategy_name = "sma"  # options: sma, momentum, mean_reversion

if strategy_name == "sma":
    from Engine.strategy import SmaCrossStrategy
    strategy = SmaCrossStrategy()
elif strategy_name == "momentum":
    from Engine.momentum import MomentumStrategy
    strategy = MomentumStrategy(lookback=10, threshold=0.02)
elif strategy_name == "mean_reversion":
    from Engine.mean_reversion import MeanReversionStrategy
    strategy = MeanReversionStrategy(window=20, threshold=0.03)
else:
    raise ValueError("Unknown strategy!")

# Download stock data
df = yf.download("AAPL", start="2022-01-01", end="2024-12-31")
engine = BacktestEngine(
    df,
    strategy,
    initial_cash=100000,
    slippage_pct=0.001,
    fee_per_trade=1.0,
    stop_loss_pct=0.03,       # 3% stop loss
    take_profit_pct=0.05      # 5% take profit
)
# Run backtest
results = engine.run()

from Engine.metrics import (
    calculate_sharpe_ratio,
    calculate_max_drawdown,
    calculate_cagr,
    calculate_num_trades,
    calculate_win_rate
)

portfolio_values = results['Portfolio Value'].dropna().values
signals = results['Signal'].fillna(0)

# Calculate duration in years
days = (results.index[-1] - results.index[0]).days
years = days / 365.25

# Call metrics
sharpe = calculate_sharpe_ratio(portfolio_values)
max_dd = calculate_max_drawdown(portfolio_values)
cagr = calculate_cagr(portfolio_values, years)
num_trades = calculate_num_trades(signals)
win_rate = calculate_win_rate(results)

# Print them
print("📊 Strategy Performance:")
print(f"• Sharpe Ratio      : {sharpe}")
print(f"• Max Drawdown      : {max_dd}%")
print(f"• CAGR              : {cagr}%")
print(f"• Number of Trades  : {num_trades}")
print(f"• Win Rate          : {win_rate}%")


# Plot results
initial_cash = 100000
plt.figure(figsize=(14,7))
plt.plot(results['Portfolio Value'], label='SMA Strategy')
plt.plot(results['Close'] / results['Close'].iloc[0] * initial_cash, label='Buy & Hold')
plt.title("Strategy vs Buy & Hold")
plt.xlabel("Date")
plt.ylabel("Portfolio Value")
plt.legend()
plt.grid(True)
plt.show()
