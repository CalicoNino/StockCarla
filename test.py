import requests
import datetime
import pandas as pd
import os
from dotenv import load_dotenv

def search_endpoint(api_key, keywords = ""):
    data = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='+keywords+'&apikey='+api_key)
    data = data.json(); data = data['bestMatches']
    titles = sorted(data[0].keys())
    search = pd.DataFrame(columns = [i[3:].title() for i in titles])

    for result in data:
        search.loc[-1,:] = [float(result[i]) if "Score" in i else datetime.datetime.strptime(result[i],'%H:%M').time() if "market" in i else result[i] for i in titles]
        search.index = search.index + 1

    search = search.iloc[::-1]

    return search
    
load_dotenv()
api_key = os.getenv("API_KEY")
symbol = 'FB'
print(search_endpoint(api_key, symbol))