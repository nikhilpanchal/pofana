import pandas as pd
from datetime import date
from position.Portfolio import Portfolio


def run_analytics(start_date, end_date):

    date_range = pd.date_range(start_date, end_date)
    portfolio = Portfolio()
    portfolio.calculate_portfolio_metrics(date_range)


if __name__ == '__main__':
    start_date = date(2016, 1, 1)
    end_date = date.today()
    run_analytics(start_date, end_date)
