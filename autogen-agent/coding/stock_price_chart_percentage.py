# filename: stock_price_chart_percentage.py
import yfinance as yf
import matplotlib.pyplot as plt

# Retrieve historical stock price data using yfinance
df_byd = yf.download('002594.SZ', start='2021-01-01', end='2021-12-31')
df_tsla = yf.download('TSLA', start='2021-01-01', end='2021-12-31')

# Calculate the percentage change in stock price
byd_price_change = (df_byd['Close'] - df_byd['Close'].iloc[0]) / df_byd['Close'].iloc[0] * 100
tsla_price_change = (df_tsla['Close'] - df_tsla['Close'].iloc[0]) / df_tsla['Close'].iloc[0] * 100

# Plot the YTD stock price change
plt.plot(byd_price_change.index, byd_price_change, label='BYD')
plt.plot(tsla_price_change.index, tsla_price_change, label='TSLA')

# Set x-axis and y-axis labels
plt.xlabel('Date')
plt.ylabel('Percentage Change')

# Set chart title
plt.title('YTD Stock Price Change (%) for BYD and TSLA')

# Show legend
plt.legend()

# Display the plot
plt.show()