import backtrader as bt

class BollingerZoneStrategy(bt.Strategy):
    params = (
        ("period", 20),
        ("devfactor", 2.0),
        ("seuil_pct", 0.10),
        ("size", 0.05),
    )

    def __init__(self):
        self.base_data = self.datas[0]      # e.g., 15m, 30m
        self.higher_tf_data = self.datas[1] # e.g., 4h

        # Bollinger on higher timeframe (resampled data)
        self.bb = bt.indicators.BollingerBands(
            self.higher_tf_data.close,
            period=self.p.period,
            devfactor=self.p.devfactor
        )

        self.order = None

    def next(self):
        # Wait until Bollinger Bands are ready
        if len(self.higher_tf_data) < self.p.period:
            return

        lower = self.bb.bot[0]
        upper = self.bb.top[0]
        distance = upper - lower
        buy_zone_high = lower + self.p.seuil_pct * distance
        sell_zone_low = upper - self.p.seuil_pct * distance

        position = self.broker.getposition(self.base_data)
        position_size = position.size

        if position_size == 0 and self.base_data.low[0] <= buy_zone_high:
            if self.order:
                self.cancel(self.order)
                self.order = None
            self.order = self.buy(
                size=self.p.size,
                exectype=bt.Order.Limit,
                price=buy_zone_high
            )
            print(f"[BUY] Limit at {buy_zone_high:.2f} | Price: {self.base_data.close[0]:.2f}")

        elif position_size > 0 and self.base_data.high[0] >= sell_zone_low:
            if self.order:
                self.cancel(self.order)
                self.order = None
            self.order = self.sell(
                size=position_size,
                exectype=bt.Order.Limit,
                price=sell_zone_low
            )
            print(f"[SELL] Limit at {sell_zone_low:.2f} | Price: {self.base_data.close[0]:.2f}")

    def notify_order(self, order):
        if order.status == bt.Order.Completed:
            action = "BUY" if order.isbuy() else "SELL"
            print(f"[{action} FILLED] Price: {order.executed.price:.2f}")
            self.order = None
        elif order.status in [bt.Order.Canceled, bt.Order.Rejected]:
            print(f"[ORDER {order.Status[order.status]}] Ref {order.ref}")
            self.order = None
