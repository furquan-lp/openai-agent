# filename: stock_price_chart.py
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Retrieve historical stock price data using yfinance
byd = yf.download("BYD", start="2022-01-01", end="2022-12-31")
tsla = yf.download("TSLA", start="2022-01-01", end="2022-12-31")

# Filter the data for the current year
byd_ytd = byd.loc[byd.index.year == pd.to_datetime('today').year]
tsla_ytd = tsla.loc[tsla.index.year == pd.to_datetime('today').year]

# Plot the YTD stock price change
plt.plot(byd_ytd.index, byd_ytd['Close'], label='BYD')
plt.plot(tsla_ytd.index, tsla_ytd['Close'], label='TSLA')

# Set x-axis and y-axis labels
plt.xlabel('Date')
plt.ylabel('Stock Price')

# Set chart title
plt.title('YTD Stock Price Change for BYD and TSLA')

# Show legend
plt.legend()

# Display the plot
plt.show()