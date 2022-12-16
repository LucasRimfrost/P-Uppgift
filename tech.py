import time
import datetime
import pandas as pd
import mplfinance as mpf


# Gathering tech data from query url
def gather_tech_data(ticker):

    period1 = int(time.mktime((datetime.datetime.today() - datetime.timedelta(days=30)).timetuple()))
    period2 = int(time.mktime(datetime.datetime.today().timetuple()))
    interval = "1d"
    query_url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true"

    # Read downloaded data as csv file layout
    df = pd.read_csv(query_url, index_col=0, parse_dates=True)

    # Getting price change percentage and converting to two decimals
    price_change = ((df['Close'][-1] - df['Close'][0]) / df['Close'][0]) * 100
    price_change = f"{price_change:.2f}"

    stock_price_high = df['High'].max()
    stock_price_low = df['Low'].min()

    # Configuring plot colors
    colors = mpf.make_marketcolors(up="#00ff00",
                                   down="#ff0000",
                                   wick="inherit",
                                   edge="inherit",
                                   volume="in")

    # Configuring plot style
    mpf_style = mpf.make_mpf_style(base_mpf_style="nightclouds", marketcolors=colors)

    df['SMA'] = df.Close.rolling(window=5).mean()
    df['stddev'] = df.Close.rolling(window=5).std()
    df['Upper'] = df.SMA + 2 * df.stddev
    df['Lower'] = df.SMA - 2 * df.stddev

    df = df.dropna()

    subplots = df[['Upper', 'Lower']]
    make_subplots = mpf.make_addplot(subplots)

    fig, ax = mpf.plot(df, addplot=make_subplots,
                       type="candle",
                       style=mpf_style,
                       volume=True,
                       returnfig=True,
                       title=ticker
                       )
    # Return dictionary with variables
    data = {
        'df': df,
        'price_change': price_change,
        'stock_price_low': stock_price_low,
        'stock_price_high': stock_price_high,
        'mpf_style': mpf_style,
        'make_subplots': make_subplots,
        'fig': fig
    }

    return data
