import os
import requests
import json
import datetime
import pandas as pd

def get_current_currencies():
    url = "https://api.coinbase.com/v2/exchange-rates?currency=USD"
    response = requests.get(url)
    currencies = json.loads(response.text)["data"]["rates"]

    # Convert exchange rates to USD
    for currency in currencies:
        currencies[currency] = 1/float(currencies[currency])

    # Add timestamp for each price
    current_date_time = datetime.datetime.now()
    rounded_date_time = current_date_time.replace(second=0, microsecond=0, minute=0) + datetime.timedelta(hours=round(current_date_time.minute / 60))

    # Add time to front of dictionary
    timed_currencies = {"date": str(rounded_date_time)}
    timed_currencies.update(currencies)

    # Reformat data
    data = [timed_currencies]

    # Convert to Pandas df
    df = pd.DataFrame.from_dict(data)

    # Write to CSV
    if os.path.getsize('./data/data.csv') == 0:
        df.to_csv('./data/data.csv', index=False)        
    else:
        df.to_csv('./data/data.csv', mode='a', index=False, header=False)


if __name__ == "__main__":
    timed_currencies = {}
    try:
        get_current_currencies()
        print("Data fetched successfully")
    except Exception as e:
        print(e)
        print("Error getting data")