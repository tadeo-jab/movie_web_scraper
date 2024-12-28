import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json
import sys
import re
import math
from random import choice

def scrape_data_main(query, env):
    new_query = json.loads(query)
    scraping_env = json.loads(env)

    return {"name": str(new_query), "img": str(scraping_env)}

if __name__ == "__main__":
    data = scrape_data_main(sys.argv[1], sys.argv[2])
    print(json.dumps(data))

