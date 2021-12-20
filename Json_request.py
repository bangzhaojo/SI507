import json
import requests

my_api_key = "2e188ed2ce0b42a2b46d90d442a6c648"

url = "https://api.covidactnow.org/v2/counties.json?apiKey=" + my_api_key

def requestapi(url):
    mydata = requests.get(url)
    myjson = json.loads(mydata.text)
    
    return myjson

myjson = requestapi(url)

with open('covid_19.json', 'w') as f:
    json.dump(myjson, f, indent = 4)