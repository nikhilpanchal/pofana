import pandas as pd
import numpy as np
from datetime import date, datetime

from refdata.marketdata import MarketData


class Portfolio():
    def __init__(self):
        self.positions = pd.DataFrame(
            data={
                "Symbol": ["IBM", "GOOG", "NFLX", "WMT", "M"],
                # "Country": ["US", "US", "UK", "UK", "US"],
                "quantity": [100, 200, 300, 400, 500]
            }
            # index=pd.Index(
            #     name="Symbol",
            #     data=["IBM", "GOOG", "NFLX", "WMT", "M"]
            # )
        )
        # self.positions["Market Value"] = self.positions["quantity"] * self.positions["purchase_price"]

    def calculate_portfolio_metrics(self, date_range):
        portfolio = pd.DataFrame(np.nan,
                                 columns=["Invested Amount", "Market Value"],
                                 index=date_range)

        portfolio["Invested Amount"][0] = 237430
        portfolio.fillna(method="ffill", inplace=True)

        dates = date_range.date
        prices = MarketData.get_market_prices(self.positions["Symbol"],
                                              dates[0],
                                              dates[len(dates) - 1])
        print(prices.head())
        print(self.positions)

        portfolio["Market Value"] = prices \
            .multiply(self.positions.quantity, axis="columns") \
            .sum(axis="columns")

        portfolio["Market Value"] = portfolio["Market Value"].fillna(method="ffill").fillna(0)
        portfolio["1-Day Return"] = portfolio["Market Value"].pct_change(1).fillna(0)

        # print(portfolio.head())

    def calculate_groups(self):
        positions = self.positions.loc[:, ["Country", "Market Value", "quantity"]]
        # positions.index = None
        positions["Sector"] = ["Technology"] * 3 + ["Retail"] * 2
        # print(positions)
        pos_by_sector = positions.groupby(["Country", "Sector"])
        print(pos_by_sector.sum())

    def __check_time(self, op):
        st = datetime.now()
        op()
        print("Time Taken for op: ", (datetime.now() - st).microseconds, " microseconds")

    def calculate_portfolio_symbol_metrics(self, start_date, end_date):
        result = MarketData.get_market_stats(self.positions["Symbol"], start_date, end_date)
        market_data = result[0]
        sorted_returns = result[1]

        start = datetime.now()

        self.positions["Market Data"] = market_data.ix["Prices", 0, :].values * self.positions["quantity"]

        periodic_return_data = self.get_returns_data(market_data)
        shock_data = self.get_shock_data(market_data)
        var_data = self.get_var_data(sorted_returns)

        self.positions = pd.concat([self.positions, periodic_return_data, shock_data, var_data], axis=1)

        time_taken = (datetime.now() - start).microseconds / 1000

        print(self.positions)
        print("Time Taken ", time_taken, " milliseconds")

    def get_var_data(self, sorted_returns):
        var_confidences = [95, 99]
        final_index = len(sorted_returns.index)

        indexes = [int((1 - confidence/100)*final_index) for confidence in var_confidences]
        vars_df = sorted_returns.iloc[indexes].T.reindex(self.positions["Symbol"]).reset_index(drop=True)
        vars_df.columns = ["VAR 95%", "VAR 99%"]

        return vars_df.multiply(self.positions["Market Data"], axis="index")

    def get_returns_data(self, market_data):
        one_day_returns = market_data["1-Day-Returns"]

        def format_returns(x):
            return (x.product() - 1) * 100

        returns_df = pd.DataFrame()

        returns_df["1-Day-Return"] = one_day_returns[-1:].apply(format_returns).T.reindex(self.positions["Symbol"]).values
        returns_df["1-Week-Return"] = one_day_returns[-5:].apply(format_returns).reindex(self.positions["Symbol"]).values
        returns_df["1-Month-Return"] = one_day_returns[-20:].apply(format_returns).reindex(self.positions["Symbol"]).values
        returns_df["3-Month-Return"] = one_day_returns[-60:].apply(format_returns).reindex(self.positions["Symbol"]).values

        return returns_df

    def get_shock_data(self, market_data):
        # end_prices = market_data["Prices"][-1:].T.squeeze().reindex(self.positions["Symbol"])
        # market_values = end_prices.values * self.positions["quantity"]
        market_values = self.positions["Market Data"]

        shock_df = pd.DataFrame()
        shock_df["+1% Shock"] = market_values * 1.01
        shock_df["-1% Shock"] = market_values * 0.99
        shock_df["+5% Shock"] = market_values * 1.05
        shock_df["-5% Shock"] = market_values * 0.95

        return shock_df
