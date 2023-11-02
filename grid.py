import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

class GridTradingBot:
    def __init__(self, symbol, start_date, end_date, num_levels, period, interval):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.num_levels = num_levels
        self.period = period
        self.interval = interval
        self.data = None
        self.points = None
        self.buy_points = []
        self.sell_points = []
        self.buy_index = []
        self.sell_index = []
        self.transactions = []
        self.account = 100

    def fetch_data(self):
        self.data = yf.download(self.symbol, start=self.start_date, end=self.end_date, interval=self.interval)

    def calculate_points(self, price1, price2, num_grids):
        self.points = np.linspace(price1, price2, num_grids + 2)[1:-1]
        self.points_dict = {}
        self.trade_dict = {}

        for k in range(len(self.points)):
            self.points_dict[k] = False
            self.trade_dict[k] = None

        print("Points:", self.points)

    def generate_signals(self):
        highest_grid = max(self.points_dict.keys())
        for i in range(len(self.data) - 1):
            for j in range(1, len(self.points_dict)):
                if self.data.iloc[i, :].Close > self.points[j] and self.data.iloc[i + 1, :].Close < self.points[j] and self.points_dict[j] == False:
                    if j == highest_grid:
                        self.buy_index.append(i)
                        self.buy_points.append(self.data.iloc[i + 1, :].Close)
                        self.points_dict[j] = True
                        self.trade_dict[j] = self.data.iloc[i + 1, :].Close
                        self.transactions.append(("Buy", self.data.index[i + 1]))

                elif self.data.iloc[i, :].Close < self.points[j] and self.data.iloc[i + 1, :].Close > self.points[j] and self.points_dict[j - 1] == True:
                    if j != highest_grid:
                        self.sell_index.append(i)
                        self.sell_points.append(self.data.iloc[i + 1, :].Close)
                        self.points_dict[j - 1] = False
                        self.trade_dict[j] = None
                        self.transactions.append(("Sell", self.data.index[i + 1]))

    def plot_data(self):
        plt.plot(self.data.Close)
        for point in self.points:
            plt.axhline(y=point, color='r')
        plt.plot(self.data.index[self.data.index.isin(self.buy_points)], self.data.Close[self.data.index.isin(self.buy_points)], 'go', label='Buy')
        plt.plot(self.data.index[self.data.index.isin(self.sell_points)], self.data.Close[self.data.index.isin(self.sell_points)], 'ro', label='Sell')
        plt.legend()
        plt.show()

    def sort_transactions(self):
        sorted_transactions = sorted(self.transactions, key=lambda x: x[1])
        for transaction in sorted_transactions:
            print(transaction[0] + ":", transaction[1])

    def run(self):
        self.fetch_data()
        price1 = 140
        price2 = 230
        num_grids = 5
        self.calculate_points(price1, price2, num_grids)
        self.generate_signals()
        self.plot_data()
        self.sort_transactions()

# Create an instance of the GridTradingBot class and run it
bot = GridTradingBot("BURCE.IS", start_date="2023-06-06 00:00:00", end_date="2023-07-05 00:00:00", num_levels=5, period="1d", interval="1d")
bot.run()
