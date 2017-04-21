import pandas as pd
import numpy as np

from datetime import date

from refdata.marketdata import MarketData


class Portfolio():
    def __init__(self):
        self.positions = pd.DataFrame(
            data={
                "quantity": [100, 200, 300, 400, 500],
                "purchase_price": [20, 30, 40, 50, 60],
                "purchase_date": [date(2016, 4, 19),
                                  date(2016, 5, 19),
                                  date(2016, 6, 19),
                                  date(2016, 7, 19),
                                  date(2016, 8, 19)]
            },
            index=pd.Index(
                name="Symbol",
                data=["IBM", "GOOG", "NFLX", "WMT", "M"]
            )
        )
        self.positions["Market Value"] = self.positions["quantity"] * self.positions["purchase_price"]

    def calculate_portfolio_metrics(self, date_range):
        portfolio = pd.DataFrame(np.nan,
                                 columns=["Invested Amount", "Market Value"],
                                 index=date_range)

        portfolio["Invested Amount"][0] = 237430
        portfolio.fillna(method="ffill", inplace=True)

        dates = date_range.date
        prices = MarketData.get_market_prices(self.positions.index.values,
                                              dates[0],
                                              dates[len(dates) - 1])

        portfolio["Market Value"] = prices \
            .multiply(self.positions.quantity, axis="columns") \
            .sum(axis="columns")

        portfolio["Market Value"] = portfolio["Market Value"].fillna(method="ffill").fillna(0)
        portfolio["1-Day Return"] = portfolio["Market Value"].pct_change(1).fillna(0)
        portfolio["1-Month Return"] = portfolio["Market Value"].pct_change(30).fillna(0)
        portfolio["Return"] = (portfolio["Market Value"] - portfolio["Invested Amount"]) / portfolio["Invested Amount"]

        print(portfolio)
