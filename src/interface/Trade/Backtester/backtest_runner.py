from src.exchange.gateio.GateMarketManV2 import GateIoMarketManV2
from Strategies.bollinger_zone import BollingerZoneStrategy
import backtrader as bt
from datetime import datetime

def run_backtest():
    gate = GateIoMarketManV2()
    
    df = gate.get_full_ohlcv_dataframe(
        currency_pair="BTC_USDT",
        interval="4h",  # Fetch in 1h for flexibility
        start=datetime(2024, 12, 1),
        end=datetime(2025, 1, 2)
    )

    df.index.name = 'datetime'

    # Base feed (treated as 1h)
    data_base = bt.feeds.PandasData(
        dataname=df,
        timeframe=bt.TimeFrame.Minutes,
        compression=240,
        open='open',
        high='high',
        low='low',
        close='close',
        volume='volume'
    )

    cerebro = bt.Cerebro()
    
    # Add 1h base data
    cerebro.adddata(data_base)

    # Resample to 4h
    data_4h = cerebro.resampledata(data_base, timeframe=bt.TimeFrame.Minutes, compression=240)

    # Strategy
    cerebro.addstrategy(BollingerZoneStrategy)

    cerebro.broker.setcash(10000.0)

    # Analyzers
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

    print("⏳ Running backtest...")
    result = cerebro.run()
    strat = result[0]

    print("\n📊=== BACKTEST RESULTS ===")
    print("Initial Cash: 10000")
    print("Final Portfolio Value:", cerebro.broker.getvalue())

    print("\n📉 Drawdown:")
    try:
        dd = strat.analyzers.drawdown.get_analysis()
        print(f"  Max Drawdown: {dd['max']['drawdown']:.2f}%")
    except:
        print("  ❌ No drawdown data.")

    print("\n📈 Sharpe Ratio:")
    try:
        sharpe = strat.analyzers.sharpe.get_analysis()
        print(f"  Sharpe Ratio: {sharpe.get('sharperatio', 'N/A')}")
    except:
        print("  ❌ No sharpe data.")

    print("\n🧾 Trades:")
    try:
        trades = strat.analyzers.trades.get_analysis()
        total = trades.total.closed
        wins = trades.won.total
        losses = trades.lost.total
        pnl_net = trades.pnl.net.total

        print(f"  Total Trades: {total}")
        print(f"  Wins: {wins}")
        print(f"  Losses: {losses}")
        print(f"  Win Rate: {(wins / total * 100):.2f}%" if total else "  Win Rate: N/A")
        print(f"  Net Profit: {pnl_net:.2f}")
    except:
        print("  ❌ No trades executed.")

    cerebro.plot(style='candlestick')


if __name__ == "__main__":
    run_backtest()
