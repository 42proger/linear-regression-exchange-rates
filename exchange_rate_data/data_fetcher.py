import requests
import pandas as pd
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup

def get_data():
    # Data for the request
    api_url = 'http://api.cba.am/exchangerates.asmx'
    iso_codes = 'USD'
    start_date = '2023-09-01'
    end_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Perform the POST request to the API
    request_body = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <ExchangeRatesByDateRangeByISO xmlns="http://www.cba.am/">
          <ISOCodes>{iso_codes}</ISOCodes>
          <DateFrom>{start_date}</DateFrom>
          <DateTo>{end_date}</DateTo>
        </ExchangeRatesByDateRangeByISO>
      </soap:Body>
    </soap:Envelope>
    """
    request_headers = {'Content-Type': 'text/xml; charset=utf-8', 'SOAPAction': 'http://www.cba.am/ExchangeRatesByDateRangeByISO'}
    response = requests.post(api_url, data=request_body, headers=request_headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'xml')
        data = []

        for entry in soup.find_all('ExchangeRatesByRange'):
            rate_date = datetime.strptime(entry.find('RateDate').text, "%Y-%m-%dT%H:%M:%S%z").date()

            rate = float(entry.find('Rate').text)
            data.append([rate_date, rate])

        # Create a DataFrame
        df = pd.DataFrame(data, columns=['Date', 'Rate'])
        return df

    else:
        print(f"HTTP Error: {response.status_code}")
        return None