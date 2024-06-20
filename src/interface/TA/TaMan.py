import numpy as np
import pandas as pd

class TaMan:
    def __init__(self, price_data):
        """
        Initialize with price data.
        :param price_data: pandas Series of price data
        """
        self.price_data = price_data
    
    def bollingerBands(self, window=20):
        """
        Calculate the Bollinger Bands.
        :param window: int, the window size for moving average and standard deviation
        :return: tuple of (lower_band, middle_band, upper_band)
        """
        # Calculate the moving average (middle band)
        middle_band = self.price_data.rolling(window=window).mean()
        
        # Calculate the standard deviation
        std_dev = self.price_data.rolling(window=window).std()
        
        # Calculate the upper and lower bands
        upper_band = middle_band + (std_dev * 2)
        lower_band = middle_band - (std_dev * 2)
        
        return lower_band, middle_band, upper_band

    def mm(self, window=20):
        """
        Calculate the moving average.
        :param window: int, the window size for moving average
        :return: pandas Series of moving average
        """
        return self.price_data.rolling(window=window).mean()

# Example usage
if __name__ == "__main__":
    # Sample price data
    data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])

    # Initialize the TaMan class with price data
    ta = TaMan(data)
    
    # Calculate Bollinger Bands
    lower_band, middle_band, upper_band = ta.bollingerBands()
    print("Lower Band:\n", lower_band)
    print("Middle Band:\n", middle_band)
    print("Upper Band:\n", upper_band)
    
    # Calculate Moving Average
    moving_avg = ta.mm()
    print("Moving Average:\n", moving_avg)
