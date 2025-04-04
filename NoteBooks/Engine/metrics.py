import numpy as np

def calculate_sharpe_ratio(portfolio_values, risk_free_rate=0.0, trading_days=252):
    returns = np.diff(portfolio_values) / portfolio_values[:-1]
    excess_returns = returns - risk_free_rate / trading_days
    sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns)
    return round(sharpe_ratio * np.sqrt(trading_days), 2)

def calculate_max_drawdown(portfolio_values):
    peak = portfolio_values[0]
    max_dd = 0
    for value in portfolio_values:
        if value > peak:
            peak = value
        dd = (peak - value) / peak
        max_dd = max(max_dd, dd)
    return round(max_dd * 100, 2)

def calculate_cagr(portfolio_values, num_years):
    start = portfolio_values[0]
    end = portfolio_values[-1]
    cagr = (end / start) ** (1 / num_years) - 1
    return round(cagr * 100, 2)

def calculate_num_trades(signals):
    return int((signals == 1).sum() + (signals == -1).sum()) // 2

def calculate_win_rate(df):
    trades = []
    in_position = False
    entry_price = 0

    for i in range(len(df)):
        row = df.iloc[i]
        signal = int(row['Signal'])
        price = float(row['Close'])

        if signal == 1 and not in_position:
            in_position = True
            entry_price = price
        elif signal == -1 and in_position:
            in_position = False
            profit = price - entry_price
            trades.append(profit)

    if not trades:
        return 0

    wins = sum(1 for p in trades if p > 0)
    return round(wins / len(trades) * 100, 2)
