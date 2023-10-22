# filename: stock_price_ytd.py

import requests
import pandas as pd
import matplotlib.pyplot as plt

# 1. Scraping data from Yahoo Finance

# function to scrape stock data from Yahoo Finance
def scrape_stock_data(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}/history?p={symbol}"
    response = requests.get(url)
    data = pd.read_html(response.text)
    return data[0]

# scrape BYD stock data
byd_data = scrape_stock_data("BYD")

# scrape TSLA stock data
tsla_data = scrape_stock_data("TSLA")

# 2. Parsing and cleaning the data

# keep only required columns
byd_data = byd_data[["Date", "Close*"]]
tsla_data = tsla_data[["Date", "Close*"]]

# set proper column names
byd_data.columns = ["Date", "BYD"]
tsla_data.columns = ["Date", "TSLA"]

# convert Date column to datetime object
byd_data["Date"] = pd.to_datetime(byd_data["Date"])
tsla_data["Date"] = pd.to_datetime(tsla_data["Date"])

# set Date column as the index
byd_data = byd_data.set_index("Date")
tsla_data = tsla_data.set_index("Date")

# merge the two dataframes based on Date
merged_data = pd.merge(byd_data, tsla_data, on="Date")

# 3. Plotting the chart

# create a new column with the YTD price change for BYD and TSLA
merged_data["BYD YTD"] = (merged_data["BYD"] / merged_data["BYD"].iloc[0] - 1) * 100
merged_data["TSLA YTD"] = (merged_data["TSLA"] / merged_data["TSLA"].iloc[0] - 1) * 100

# plot the chart
plt.figure(figsize=(12, 6))
plt.plot(merged_data.index, merged_data["BYD YTD"], label="BYD")
plt.plot(merged_data.index, merged_data["TSLA YTD"], label="TSLA")
plt.title("YTD Stock Price Change")
plt.xlabel("Date")
plt.ylabel("Price Change (%)")
plt.legend()
plt.grid(True)
plt.show()