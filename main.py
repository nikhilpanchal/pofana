import pandas as pd
from datetime import date
from position.Portfolio import Portfolio


def run_analytics(start_date, end_date):
    end_date = end_date.replace(day=end_date.day-2)
    date_range = pd.date_range(start_date, end_date)
    portfolio = Portfolio()
    portfolio.calculate_portfolio_symbol_metrics(start_date, end_date)
    # portfolio.calculate_portfolio_metrics(date_range)
    # portfolio.calculate_groups()


if __name__ == '__main__':
    pd.set_option('display.expand_frame_repr', False)

    start_date = date(2016, 1, 1)
    end_date = date.today()
    run_analytics(start_date, end_date)
