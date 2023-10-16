import matplotlib.pyplot as plt
import pandas as pd
from datetime import date, timedelta
from exchange_rate_data.data_fetcher import get_data
from scipy import stats

def main():
    data = get_data()
    print(data)

    # Calculate the linear regression
    x = [i.toordinal() for i in data['Date']]
    y = data['Rate'].values

    slope, intercept, r, p, std_err = stats.linregress(x, y)

    regression = [slope * x_value + intercept for x_value in x]

    # Calculate forecasting
    last_day = x[-1]
    forecast = slope * last_day + intercept

    # Retrieve the real exchange rate
    real_rate = y[-1]

    print("Forecast:", forecast)
    print("Real Rate:", real_rate)

    # Plot the data and regression line
    x_dates = [date.fromordinal(int(x_value)) for x_value in x]
    plt.scatter(x_dates, y, c='gray', label='Exchange Rates')
    plt.plot(x_dates, regression, c='b', label='Linear Regression')
    plt.scatter(x_dates[-1], real_rate, c='g', label='Real Rate')
    plt.scatter(x_dates[-1], forecast, c='r', label='Forecast')

    plt.xticks(x_dates, rotation=45)

    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()