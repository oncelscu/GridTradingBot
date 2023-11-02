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
        self.profits = []
        self.positions = None
   
   
    def fetch_data(self):
        self.data = yf.download(self.symbol, start=self.start_date, end=self.end_date, period=self.period, interval=self.interval)

    def calculate_points(self):
        start_price = 110
        end_price = 170
        self.points = np.flip(np.linspace(end_price, start_price, self.num_levels + 1))
        self.points_dict = {}
        self.trade_dict = {}
        
        for k in range(len(self.points)):  # Fixed issue: added self prefix
            self.points_dict[k] = False
            self.trade_dict[k] = None
           
        print("Points:", self.points)
        
    def grid_positions(self):
        self.buy_positions_dict = {}
        self.sell_positions_dict = {}

    def check_the_points(self):
         for i in range(len(self.data) - 1):
            for j in range(1, len(self.points_dict)):
                if self.data.iloc[i].Close > self.points[j] and self.data.iloc[i + 1].Close < self.points[j] and self.points_dict[j] == False:
                    self.buy_index.append(i)  # Fixed issue: use i instead of i+1
                    self.buy_points.append(self.data.iloc[i + 1].Close)
                    self.points_dict[j] = True
                    self.trade_dict[j] = self.data.iloc[i + 1].Close
                    self.transactions.append(("Buy", self.data.index[i + 1]))
                    
                elif self.data.iloc[i].Close < self.points[j] and self.data.iloc[i + 1].Close > self.points[j] and self.points_dict[j - 1] == True:
                    self.sell_index.append(i)  # Fixed issue: use i instead of i+1
                    self.sell_points.append(self.data.iloc[i + 1].Close)
                    self.points_dict[j - 1] = False
                    print(self.data.iloc[i + 1].Close, self.trade_dict[j - 1])
                    self.trade_dict[j] = None
                    self.transactions.append(("Sell", self.data.index[i + 1]))

    def plot_data(self):
        plt.plot(self.data.Close)
        for point in self.points:
            plt.axhline(y=point, color='r')
        plt.plot(self.data.index[self.buy_index], self.data.Close.iloc[self.buy_index], 'go', label='Buy')
        plt.plot(self.data.index[self.sell_index], self.data.Close.iloc[self.sell_index], 'ro', label='Sell')
        plt.legend()
        plt.show()
            
    def sort_transactions(self):
        sorted_transactions = sorted(self.transactions, key=lambda x: pd.to_datetime(x[1]))
        for transaction in sorted_transactions:
            print(transaction[0] + ":", transaction[1])
            
    def display_trade_points(self):
        sorted_trade_points = sorted(zip(self.buy_points, self.sell_points))
        for i, (buy_point, sell_point) in enumerate(sorted_trade_points):
            print("Trade", i + 1)
            print("Buy Point:", buy_point)
            print("Sell Point:", sell_point)
            print()
    
    def calculate_profits(self):
        num_trades = min(len(self.buy_points), len(self.sell_points))
        for i in range(num_trades):
            buy_price = self.buy_points[i]
            sell_price = self.sell_points[i]
            profit = sell_price - buy_price
            self.profits.append(profit)

            # Check if the current trade is in between two grids
            if i + 1 < num_trades:
                previous_buy_price = self.buy_points[i + 1]
                if buy_price < previous_buy_price:
                    profit = -profit

        return self.profits
       
    def run(self):
        self.fetch_data()
        self.calculate_points()
        self.check_the_points()
        self.plot_data()
        self.sort_transactions()
        self.calculate_profits()
        self.display_trade_points()
        self.display_profits()
    
    def display_profits(self):
        for i in range(len(self.profits)):
            print("Trade", i + 1, "Profit:", self.profits[i])

# Create an instance of the GridTradingBot class and run it
bot = GridTradingBot("THYAO.IS", start_date="2023-01-01", end_date="2023-07-05", num_levels=4, period="1d", interval="1h")
bot.run()

