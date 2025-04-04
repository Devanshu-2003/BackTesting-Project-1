# 📈 Backtesting Engine

A modular backtesting engine for simulating and evaluating trading strategies like SMA Crossover, Momentum, and Mean Reversion. Built using **Python**, **pandas**, and **Streamlit**, this engine helps you test strategies, tune parameters, visualize performance, and compare against Buy & Hold.

---

## 🚀 Features

- ✅ **SMA Crossover**, **Momentum**, and **Mean Reversion** strategies
- ✅ Modular backtesting with slippage & transaction costs
- ✅ Performance metrics: Sharpe Ratio, Max Drawdown, CAGR, Win Rate
- ✅ Interactive **Streamlit Dashboard**
- ✅ Multi-ticker support (AAPL, MSFT, GOOGL, etc.)
- ✅ Grid Search Optimization (Hyperparameter tuning)
- ✅ Clean Matplotlib visualizations

---

## 📁 Project Structure

```
BackTesting Engine/
├── Engine/
│   ├── backtester.py            # Core simulation engine
│   ├── strategy.py              # SMA strategy
│   ├── momentum.py              # Momentum strategy
│   ├── mean_reversion.py        # Mean reversion strategy
│   ├── metrics.py               # Performance evaluation
├── NoteBooks/
│   ├── main.py                  # CLI testing interface
│   ├── dashboard.py             # Streamlit UI
├── requirements.txt
└── README.md
```

---

## 🛠️ Installation

```bash
git clone https://github.com/your-username/backtesting-engine.git
cd backtesting-engine
pip install -r requirements.txt
```

---

## ⚙️ CLI Usage

Edit the strategy selector in `main.py`:
```python
strategy_name = "momentum"  # Options: "sma", "momentum", "mean_reversion"
```

Then run the script:
```bash
python NoteBooks/main.py
```

---

## 🖥️ Launch Streamlit Dashboard

```bash
streamlit run NoteBooks/dashboard.py
```

You’ll get an interactive dashboard to:
- Select strategies
- Input tickers (AAPL, MSFT, etc.)
- Change parameters (thresholds, lookback, window)
- View metrics & performance plots
- Run grid search optimization (optional)

---

## 📊 Strategies Overview

| Strategy          | Description                                                              |
|------------------|--------------------------------------------------------------------------|
| **SMA Crossover** | Buy when short-term SMA > long-term SMA, sell when it crosses below     |
| **Momentum**      | Buy if past returns exceed a threshold, sell if below negative threshold |
| **Mean Reversion**| Buy when price < MA by threshold, sell when price > MA by threshold     |

---

## 📈 Metrics Calculated

- **Sharpe Ratio**
- **Max Drawdown**
- **Compound Annual Growth Rate (CAGR)**
- **Number of Trades**
- **Win Rate**

---

## 📌 To-Do (Optional Improvements)

- [ ] Add Stop Loss / Take Profit
- [ ] Add multi-strategy backtests
- [ ] Export trades to CSV
- [ ] Compare multiple strategy metrics in a table

---

## 🧠 Built With

- [Python](https://python.org)
- [Streamlit](https://streamlit.io/)
- [Matplotlib](https://matplotlib.org/)
- [pandas](https://pandas.pydata.org/)
- [yfinance](https://github.com/ranaroussi/yfinance)

---

## 📸 Screenshot

> Example from dashboard:

![Dashboard Screenshot](https://via.placeholder.com/800x400.png?text=Insert+Screenshot+Here)

---

## 🙌 Author

**Devanshu Chudhary**  
Made with ❤️ and caffeine  
[LinkedIn](https://www.linkedin.com) • [GitHub](https://github.com/your-username)
