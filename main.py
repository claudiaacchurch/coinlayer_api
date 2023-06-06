import csv
import requests

url = "http://api.coinlayer.com/api/"
access_key = "57b1d007745fb50acbebfce6c70c107f"

#List live data for selected symbols

def get_live_data(target, symbols): #symbols in a string
    parameters = { #parameters for request
        "access_key" : access_key,
        "target": target, #target currency 
        "symbols": symbols
    }
    response = requests.get(url + "live", params=parameters)

    if response.status_code == 200:
        data = response.json() #parse json reponse into dictionary
        with open("repsonse.csv", "w") as file:
            writer = csv.writer(file) #writer object
            writer.writerow(['target', data["target"]])
            for item, val in data["rates"].items():              
                writer.writerow([item, val])
        print(data)
    else:
        print(f"Request failed with status code {response.status_code}")

get_live_data("USD", "BTC,ETH")

#List available crypto and fiat currencies, optional parameters for specified currencies; return all for any left None.

def get_symbols(crypto_currencies=None, fiat_currencies=None): #Currencies = symbol for crypto; code for fiat (list) 
    
    parameters = {
        "access_key": access_key
    }

    response = requests.get(url + "list", params=parameters)
    data = response.json()

    if response.status_code == 200:
        with open("list_data.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(["Symbol", "Name", "Full Name", "Max Supply", "Icon URL"]) #crypto headers
            #symbols = crypto parameter unless None then all of the keys in dataset
            crypto_symbols = data["crypto"].keys() if crypto_currencies is None else crypto_currencies
            for symbol in crypto_symbols:
                details = data["crypto"].get(symbol)
                if details is not None:
                    writer.writerow([ 
                        details.get('symbol', ''), #key, default value
                        details.get('name', ''),
                        details.get('name_full', ''),
                        details.get('max_supply', ''),
                        details.get('icon_url', ''),
                    ])
            writer.writerow(["Alphabetic code", "Currency"]) #fiat headers
            fiat_codes = data["fiat"].keys() if fiat_currencies is None else fiat_currencies
            for code in fiat_codes:
                currency = data["fiat"].get(code)
                if currency is not None:
                    writer.writerow([code, currency])
    else:
        print(f"Error: {response.status_code}")

get_symbols(["BTC", "ETH"], ["GBP"])

def get_historical_data(date, target, symbols):

    parameters = {
        "YYYY-MM-DD": date,
        "access_key": access_key,
        "target": target,
        "symbols": symbols
    }

    response = requests.get(url + date, params=parameters)
    if response.status_code == 200:
        data = response.json()
        with open(f"{date}.csv", "w") as file:
            writer = csv.writer(file)
        print(data)

get_historical_data("2020-10-16", "USD", "BTC")
'''
* NOT AVAILABLE ON BASIC PLAN *
#func to convert crypto to another crypto:

def crypto_converter(from_symbol, to_symbol, amount):
    endpoint = 'http://api.coinlayer.com/convert'
    parameters = {
        "access_key" : "57b1d007745fb50acbebfce6c70c107f",
        "from": from_symbol,
        "to": to_symbol,
        "amount": amount
    }

    response = requests.get(endpoint, params = parameters)
    json_data = response.json()
    data = list(map(list, json_data.items()))
    if response.status_code == 200:
        with open("repsonse.csv", "a") as file:
            file.write("\n" + "Converter:" + "\n" + "\n")
            writer = csv.writer(file, delimiter=":")
            writer.writerows(data)
    else:
        print(f"Error: {response.status_code}")

crypto_converter("BTC", "ETH", 10)

 func to get data for requested symbols in a specific timeframe:

def get_historical_data(start_date, end_date, symbol):
    timeframe_url = 'http://api.coinlayer.com/timeframe'
    parameters = {
        "access_key" : "57b1d007745fb50acbebfce6c70c107f",
        "start_date": start_date,
        "end_date": end_date,
        "symbols": symbol
    }
    response = requests.get(timeframe_url, params=parameters)
    if response.status_code == 200:
        data = response.json()
        csv_data = list(map(list, data.items()))
        with open("historical_data.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerows(csv_data)
    else:
        print(f"Request failed with status code {response.status.code}")

get_historical_data("2023-01-01", "2023-02-01", "BTC")
'''