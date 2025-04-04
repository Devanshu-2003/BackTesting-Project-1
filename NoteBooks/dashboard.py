# dashboard.py

import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

from Engine.strategy import SmaCrossStrategy
from Engine.momentum import MomentumStrategy
from Engine.mean_reversion import MeanReversionStrategy
from Engine.backtester import BacktestEngine
from Engine.metrics import (
    calculate_sharpe_ratio,
    calculate_max_drawdown,
    calculate_cagr,
    calculate_num_trades,
    calculate_win_rate
)

st.title("📈 Backtesting Dashboard")

# Sidebar inputs
strategy_name = st.sidebar.selectbox("Select Strategy", ["SMA", "Momentum", "Mean Reversion"])
ticker_options = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA"]  # Add any others you want
selected_tickers = st.sidebar.multiselect("Select Stock Tickers", options=ticker_options, default=["AAPL"])

if not selected_tickers:
    st.warning("Please select at least one stock ticker.")
    st.stop()

# Use this instead of `ticker_list = [...]`
ticker_list = selected_tickers
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-12-31"))

initial_cash = st.sidebar.number_input("Initial Cash", value=100000)
slippage_pct = st.sidebar.number_input("Slippage %", value=0.001)
fee_per_trade = st.sidebar.number_input("Fee per Trade", value=1.0)

strategy_kwargs = {}
if strategy_name == "Momentum":
    strategy_kwargs = {"lookback": 10, "threshold": 0.02}
elif strategy_name == "Mean Reversion":
    strategy_kwargs = {"window": 20, "threshold": 0.03}


# Strategy-specific params
if strategy_name == "SMA":
    strategy = SmaCrossStrategy()
elif strategy_name == "Momentum":
    lookback = st.sidebar.slider("Lookback", 5, 30, 10)
    threshold = st.sidebar.slider("Threshold", 0.0, 0.1, 0.02)
    strategy = MomentumStrategy(lookback=lookback, threshold=threshold)
elif strategy_name == "Mean Reversion":
    window = st.sidebar.slider("Window", 5, 30, 20)
    threshold = st.sidebar.slider("Threshold", 0.0, 0.1, 0.03)
    strategy = MeanReversionStrategy(window=window, threshold=threshold)

# Run backtest
def create_strategy(name, window=None, threshold=None, lookback=None):
    if name == "SMA":
        return SmaCrossStrategy()
    elif name == "Momentum":
        return MomentumStrategy(lookback=lookback, threshold=threshold)
    elif name == "Mean Reversion":
        return MeanReversionStrategy(window=window, threshold=threshold)
    else:
        raise ValueError("Invalid strategy name")

if st.button("Run Backtest"):
    df = yf.download(ticker_list, start=start_date, end=end_date, group_by='ticker', auto_adjust=True)
    strategy_kwargs = {}
    if strategy_name == "Momentum":
        strategy_kwargs = {"lookback": 10, "threshold": 0.02}
    elif strategy_name == "Mean Reversion":
        strategy_kwargs = {"window": 20, "threshold": 0.03}
    for symbol in ticker_list:
        st.subheader(f"📈 {symbol} Strategy Performance")

        try:
            symbol_df = df[symbol].dropna()
        except KeyError:
            st.warning(f"No data found for {symbol}. Skipping...")
            continue

        strategy_instance = create_strategy(strategy_name, **strategy_kwargs)
        engine = BacktestEngine(symbol_df, strategy_instance, initial_cash, slippage_pct, fee_per_trade)
        results = engine.run()

        # --- Show performance metrics ---
        portfolio_values = results['Portfolio Value'].dropna().values
        signals = results['Signal'].fillna(0)
        days = (results.index[-1] - results.index[0]).days
        years = days / 365.25

        sharpe = calculate_sharpe_ratio(portfolio_values)
        max_dd = calculate_max_drawdown(portfolio_values)
        cagr = calculate_cagr(portfolio_values, years)
        num_trades = calculate_num_trades(signals)
        win_rate = calculate_win_rate(results)

        st.write(f"**Sharpe Ratio:** {sharpe:.2f}")
        st.write(f"**Max Drawdown:** {max_dd:.2f}%")
        st.write(f"**CAGR:** {cagr:.2f}%")
        st.write(f"**Trades:** {num_trades}")
        st.write(f"**Win Rate:** {win_rate:.2f}%")

        # --- Plot portfolio value ---
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(results['Portfolio Value'], label='Strategy', linewidth=2.5)
        ax.plot(results['Close'] / results['Close'].iloc[0] * initial_cash, label='Buy & Hold', linestyle='--', linewidth=2)
        ax.set_title("Strategy vs Buy & Hold", fontsize=16, weight='bold')
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Portfolio Value", fontsize=12)
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.5)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

df = yf.download(ticker_list, start=start_date, end=end_date, group_by='ticker', auto_adjust=True)
if st.checkbox("Run Optimization Grid Search"):
    best_sharpe = float('-inf')
    best_params = None

    st.info("Running grid search over parameters...")

    for w in range(10, 31, 5):  # Example: window size 10 to 30
        for t in [0.01, 0.02, 0.03]:
            strategy = MeanReversionStrategy(window=w, threshold=t)
            engine = BacktestEngine(df[selected_tickers[0]], strategy, initial_cash, slippage_pct, fee_per_trade)
            results = engine.run()
            sharpe = calculate_sharpe_ratio(results['Portfolio Value'].dropna().values)

            if sharpe > best_sharpe:
                best_sharpe = sharpe
                best_params = (w, t)

    st.success(f"Best Sharpe Ratio: {best_sharpe:.2f} with window={best_params[0]}, threshold={best_params[1]}")
