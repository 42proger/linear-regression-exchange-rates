import matplotlib.pyplot as plt
import pandas as pd
from datetime import date, timedelta
from exchange_rate_data.data_fetcher import get_data

def main():
    data = get_data()
    print(data)

    # Calculate the linear regression
    min_date = min(data['Date'])
    data['Date'] = [(d - min_date).days for d in data['Date']]

    n = len(data['Date'])
    sum_x = data['Date'].sum()
    sum_y = data['Rate'].sum()
    sum_xy = (data['Date'] * data['Rate']).sum()
    sum_x_squared = (data['Date']**2).sum()

    w1 = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x**2)
    w0 = (sum_y - w1 * sum_x) / n

    regression = w0 + w1 * data['Date']

    # Calculate forecasting
    yesterday = (date.today() - timedelta(days=1) - min_date).days
    forecast = w0 + w1 * yesterday

    # Retrieve the real exchange rate
    real_rate = data[data['Date'] == yesterday]['Rate'].values[0]

    print("Forecast:", forecast)
    print("Real Rate:", real_rate)

    # Plot the data and regression line
    plt.scatter(data['Date'], data['Rate'], c='gray', label='Exchange Rates')
    plt.plot(data['Date'], regression, c='b', label='Linear Regression')
    plt.scatter(yesterday, real_rate, c='g', label='Real Rate')
    plt.scatter(yesterday, forecast, c='r', label='Forecast')

    date_labels = [(min_date + timedelta(days=x)).strftime("%d.%m") for x in data['Date']]
    plt.xticks(data['Date'], date_labels, rotation=45)

    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
