import os
import requests
import json
import datetime
import pandas as pd

def get_current_currencies():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum%2Cbitcoin%2Calgorand&vs_currencies=usd"
    response = requests.get(url)
    currencies = json.loads(response.text)

    # Clean data
    for coin, info in currencies.items():
        usd_amount = info['usd']
        currencies[coin] = usd_amount
        del info['usd']

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
    if os.path.getsize('./data/test.csv') == 0:
        df.to_csv('./data/test.csv', index=False)        
    else:
        df.to_csv('./data/test.csv', mode='a', index=False, header=False)


if __name__ == "__main__":
    timed_currencies = {}
    get_current_currencies()