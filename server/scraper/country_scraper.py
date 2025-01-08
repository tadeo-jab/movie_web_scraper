import requests
from bs4 import BeautifulSoup
import json
import sys

def country_scraper_main(url):
    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')

    table = (soup.find('div', class_='MdxTable_wrapper__BUynF')).table.tbody
    table_countries = table.find_all('tr')

    country_codes = {}

    for country in table_countries:
        row = country.find_all('td')
        country_codes.update({row[0].text : row[1].text})
    
    return country_codes

if __name__ == "__main__":
    utils = json.loads(sys.argv[1])

    data = country_scraper_main(utils['country_codes_url'])
    print(json.dumps({'data': data}))