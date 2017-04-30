import pandas_datareader.data as data
from datetime import date, datetime
import pandas as pd


class MarketData:
    @staticmethod
    def get_market_prices(symbols, start_date, end_date):
        prices = data.DataReader(symbols, data_source="google", start=start_date, end=end_date)
        return prices["Close"]

    @staticmethod
    def get_market_stats(symbols, start_date, end_date):
        prices = MarketData.get_market_prices(symbols, start_date, end_date)

        # Prices is a data-frame indexed by dates and a column for each symbol
        market_data_panel = pd.Panel({
            "Prices": prices
        })

        one_day_returns = prices.pct_change(1)+1
        one_day_returns = one_day_returns[1:]

        market_data_panel["1-Day-Returns"] = one_day_returns

        new_series = []
        for colname in one_day_returns:
            new_series.append(one_day_returns[colname].sort_values().reset_index()[colname])

        sorted_returns_df = pd.concat(new_series, axis=1)

        return market_data_panel, sorted_returns_df

if __name__ == '__main__':
    start = datetime.now()
    # MarketData.get_market_prices(["IBM", "GOOG"], date(2016, 1, 1), date.today())
    MarketData.get_market_stats(["IBM", "GOOG"], date(2016, 1, 1), date.today())
    print((datetime.now() - start).microseconds)
