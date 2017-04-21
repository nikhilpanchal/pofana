import pandas_datareader.data as data
from datetime import date


class MarketData:

    @staticmethod
    def get_market_prices(symbols, start_date, end_date):
        prices = data.DataReader(symbols, data_source="google", start=start_date, end=end_date)
        return prices["Close"]


if __name__ == '__main__':
    MarketData.get_market_prices(["IBM", "GOOG"], date(2016, 1, 1), date.today())