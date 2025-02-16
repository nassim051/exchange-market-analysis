import numpy as np
import pandas as pd

class TaMan:
    def __init__(self, price_data):
        """
        Initialize with price data.
        :param price_data: List of lists, where each sublist represents a candle.
        """
        self.price_data = price_data
        self.closing_prices = self._extract_closing_prices()

    def _extract_closing_prices(self):
        """
        Extract closing prices from the price data.
        :return: pandas Series of closing prices.
        """
        closing_prices = [float(candle[2]) for candle in self.price_data]  # Closing price is the 3rd element (index 2)
        return pd.Series(closing_prices)

    def calculate_bollinger_bands(self, window=20):
        """
        Calculate Bollinger Bands for the last candle based on previous candles.
        :param window: int, the window size for moving average and standard deviation.
        :return: dict, containing lower, middle, and upper bands for the last candle.
        """
        if len(self.closing_prices) < window:
            raise ValueError("Not enough data to calculate Bollinger Bands. Need at least `window` candles.")

        # Calculate Bollinger Bands
        middle_band = self.closing_prices.rolling(window=window).mean()
        std_dev = self.closing_prices.rolling(window=window).std()
        upper_band = middle_band + (std_dev * 2)
        lower_band = middle_band - (std_dev * 2)

        # Get the last values (for the last candle)
        last_lower_band = lower_band.iloc[-1]
        last_middle_band = middle_band.iloc[-1]
        last_upper_band = upper_band.iloc[-1]

        return {
            "lower_band": last_lower_band,
            "middle_band": last_middle_band,
            "upper_band": last_upper_band
        }
"""
# Example usage
price_data = [
    ['1738958400', '2296.27509950', '0.02306', '0.02337', '0.02304', '0.0232', '98847.95000000', 'true'],
    ['1738972800', '3643.27783200', '0.02433', '0.02447', '0.02301', '0.02304', '154471.96000000', 'true'],
    ['1738987200', '4731.66537730', '0.02363', '0.02469', '0.02329', '0.02434', '195875.53000000', 'true'],
    ['1739001600', '4588.83090170', '0.02315', '0.02364', '0.02241', '0.02362', '198287.85000000', 'true'],
    ['1739016000', '3849.80461370', '0.02285', '0.02335', '0.0227', '0.02314', '167022.64000000', 'true'],
    ['1739030400', '3294.33487980', '0.02253', '0.02326', '0.02228', '0.02284', '144689.45000000', 'true'],
    ['1739044800', '2198.32812740', '0.0225', '0.0226', '0.0225', '0.02256', '97552.67000000', 'true'],
    ['1739059200', '2652.74170610', '0.02229', '0.02266', '0.02229', '0.0225', '117779.39000000', 'true'],
    ['1739073600', '2898.96972460', '0.02244', '0.02258', '0.0223', '0.02251', '129091.35000000', 'true'],
    ['1739088000', '4724.90541300', '0.02209', '0.0225', '0.02183', '0.02244', '214268.43000000', 'true'],
    ['1739102400', '3010.49982410', '0.02151', '0.02215', '0.02109', '0.02209', '139755.30000000', 'true'],
    ['1739116800', '2267.81696890', '0.0214', '0.02154', '0.02127', '0.02151', '105608.09000000', 'true'],
    ['1739131200', '2038.90218170', '0.0213', '0.02154', '0.02126', '0.02141', '95432.32000000', 'true'],
    ['1739145600', '7908.10795520', '0.02058', '0.02131', '0.01888', '0.02131', '398419.16000000', 'true'],
    ['1739160000', '2674.53185670', '0.02103', '0.02126', '0.02047', '0.0206', '128801.28000000', 'true'],
    ['1739174400', '2645.55824870', '0.02164', '0.02183', '0.02089', '0.02105', '123233.47000000', 'true'],
    ['1739188800', '2399.87662930', '0.02095', '0.0217', '0.02079', '0.02163', '112311.23000000', 'true'],
    ['1739203200', '2943.46633780', '0.02139', '0.02183', '0.02063', '0.02093', '138868.91000000', 'true'],
    ['1739217600', '1940.31306660', '0.02131', '0.02144', '0.02131', '0.0214', '90844.56000000', 'true'],
    ['1739232000', '485.84144770', '0.0213', '0.02139', '0.02127', '0.02133', '22772.41000000', 'false']
]

# Initialize the class with price data
bb_calculator = TaMan(price_data)

# Calculate Bollinger Bands for the last candle
bollinger_bands = bb_calculator.calculate_bollinger_bands(window=20)

# Print the results
print("Bollinger Bands for the Last Candle:")
print(f"Lower Band: {bollinger_bands['lower_band']}")
print(f"Middle Band: {bollinger_bands['middle_band']}")
print(f"Upper Band: {bollinger_bands['upper_band']}")"""