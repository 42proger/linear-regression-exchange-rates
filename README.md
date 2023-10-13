# Linear Regression Forecasting Exchange Rates

This project obtains data from the [Central Bank of Armenia's open API](http://api.cba.am/exchangerates.asmx), covering the data from a specified start date for any of the 30 supported currencies.

| ISO   | Currency                | ISO   | Currency                |
|-------|-------------------------|-------|-------------------------|
| USD   | US Dollar               | GBP   | British Pound Sterling  |
| AUD   | Australian Dollar       | EUR   | Euro                   |
| XDR   | IMF Special Drawing Rights | IRR   | Iranian Rial          |
| PLN   | Polish Złoty           | CAD   | Canadian Dollar         |
| INR   | Indian Rupee            | NOK   | Norwegian Krone        |
| JPY   | Japanese Yen           | SEK   | Swedish Krona          |
| CHF   | Swiss Franc             | CZK   | Czech Republic Koruna  |
| CNY   | Chinese Yuan (Renminbi) | SGD   | Singapore Dollar       |
| BRL   | Brazilian Real          | AED   | UAE Dirham             |
| KGS   | Kyrgyzstani Som         | KZT   | Kazakhstani Tenge      |
| RUB   | Russian Ruble           | UAH   | Ukrainian Hryvnia      |
| UZS   | Uzbekistani Som         | BYN   | Belarusian Ruble       |
| TJS   | Tajikistani Somoni      | GEL   | Georgian Lari          |
| HKD   | Hong Kong Dollar        | XAU   | Gold (troy ounce)      |
| XAG   | Silver (troy ounce)     | NZD   | New Zealand Dollar      |

The data is then processed using linear regression to forecast exchange rate, which is compared with the actual rate.

---

## Usage/Examples

To install the necessary dependencies, once you've cloned the repo, cd to the directory in which 'requirements.txt' is located, and run 

```bash
pip3 install -r requirements.txt
```

Before proceeding, make sure to configure the exchange rate data fetching. In the `exchange_rate_data/data_fetcher.py` file, specify the ISO code of the desired currency and the start date in the format YYYY-MM-DD:

```python
iso_codes = 'USD'
start_date = '2023-09-01'
```
Once you've configured the data fetcher, you can run the application as follows:

```bash
python3 main.py
```
After executing the application, it will produce a graphical representation illustrating exchange rates, linear regression analysis, and a forecast.

---

## Linear regression

Linear regression represents a regression model that describes the relationship between one (dependent) variable and one or more other variables (factors, regressors, independent variables) with a linear functional dependency. Let's consider a linear regression model in which the dependent variable depends on only one factor. In this case, the function describing the relationship of $`y`$ with $`x`$ will have the following form:

$`f(x) = w_{0} + w_{1} \ast x`$

The task is to find the weight coefficients $`w_{0}`$ and $`w_{1}`$, such that this line best fits the original data. To achieve this, we define an error function, the minimization of which will determine the values of $`w_{0}`$ and $`w_{1}`$ using the method of least squares:

$`
\begin{aligned}
MSE = \frac{1}{n} \ast \sum\limits_{i=0}^{n}(y_{i} - f(x_{i}))^{2}
\end{aligned}
`$

Or, by substituting the model equation:

$`
\begin{aligned}
MSE = \frac{1}{n} \ast \sum\limits_{i=0}^{n}(y_{i} - w_{0} - w_{1} \ast x_{i} )^{2}
\end{aligned}
`$

Minimizing the $`MSE`$ error function involves finding the partial derivatives with respect to $`w_{0}`$ and $`w_{1}`$:

$`
\begin{aligned}
\frac{\delta MSE(w_{0}, w_{1})}{\delta w_{0}} = -\frac{2}{n} \ast \sum\limits_{i=0}^{n}(y_{i} - w_{0} - w_{1} \ast x_{i} )^{2}
\end{aligned}
`$

$`
\begin{aligned}
\frac{\delta MSE(w_{0}, w_{1})}{\delta w_{1}} = -\frac{2}{n} \ast \sum\limits_{i=0}^{n}((y_{i} - w_{0} - w_{1} \ast x_{i} ) \ast x_{i})
\end{aligned}
`$

Setting these derivatives to zero yields a system of equations whose solution minimizes the $`MSE`$:

$`\left\{
\begin{aligned}
0 &= -\frac{2}{n} \ast \sum\limits_{i=0}^{n}(y_{i} - w_{0} - w_{1} \ast x_{i}) \\
0 &= -\frac{2}{n} \ast \sum\limits_{i=0}^{n}((y_{i} - w_{0} - w_{1} \ast x_{i}) \ast x_{i})
\end{aligned}
\right.`$

Expanding the sums and taking into account that $`-\frac{2}{n}`$ cannot be equal to zero, we set the second factors to zero:

$`\left\{
\begin{aligned}
0 &= -w_{0} \ast n + \sum\limits_{i=0}^{n}y_{i} - w_{1} \ast \sum\limits_{i=0}^{n}x_{i} \\
0 &= \sum\limits_{i=0}^{n}(y_{i} \ast x_{i}) + w_{0} \ast \sum\limits_{i=0}^{n}x_{i} - w_{1} \ast \sum\limits_{i=0}^{n}x_{i}^{2}
\end{aligned}
\right.`$

We express $`w_{0}`$ from the first equation:

$`
\begin{aligned}
w_{0} = \frac{\sum\limits_{i=0}^{n}y_{i}}{n} - w_{1}\frac{\sum\limits_{i=0}^{n}x_{i}}{n}
\end{aligned}
`$

Substituting this into the second equation, we solve for $`w_{1}`$:

$`
\begin{aligned}
0 = \sum\limits_{i=0}^{n}(y_{i} \ast x_{i}) + (\frac{\sum\limits_{i=0}^{n}y_{i}}{n} - w_{1}\frac{\sum\limits_{i=0}^{n}x_{i}}{n}) \ast \sum_{i=0}^{n}x_{i} - w_{1} \ast \sum\limits_{i=0}^{n}x_{i}^{2}
\end{aligned}
`$

$`
\begin{aligned}
0 = \sum\limits_{i=0}^{n}(y_{i} \ast x_{i}) + \frac{\sum\limits_{i=0}^{n}(y_{i}\sum\limits_{i=0}^{n}x_{i})}{n} - w_{1}\frac{\sum\limits_{i=0}^{n}(x_{i}\sum\limits_{i=0}^{n}x_{i})}{n} - w_{1} \ast \sum\limits_{i=0}^{n}x_{i}^{2}
\end{aligned}
`$

By solving for $`w_{1}`$ from this equation, we obtain the analytical solution.

$`
\begin{aligned}
w_{1} = \frac{\frac{\sum\limits_{i=0}^{n}(x_{i}\sum\limits_{i=0}^{n}y_{i})}{n} - \sum\limits_{i=0}^{n}(y_{i} \ast x_{i})}{\frac{\sum\limits_{i=0}^{n}(x_{i}\sum\limits_{i=0}^{n}x_{i})}{n} - \sum\limits_{i=0}^{n}x_{i}^{2}}
\end{aligned}
`$