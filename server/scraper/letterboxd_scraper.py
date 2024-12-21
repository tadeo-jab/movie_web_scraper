import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json
import sys
import re
import math
from random import choice

filters = {
    "years": ["1890", "2024"],
    "genre": ["action", "adventure", "animation", "comedy","crime","documentary","drama","family","fantasy","history","horror","music","mystery","romance","science-fiction","thriller","tv-movie","war","western"]
}

def get_page_count(limit, regex, browser, url):
    context = browser.new_context()
    page = browser.new_page()

    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_selector("p.ui-block-heading")

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")

    count_text = soup.find(class_="ui-block-heading").text
    movie_count = int(re.search(regex, count_text).group())
    
    return math.ceil(movie_count / limit)

def get_movies(url, browser):
    context = browser.new_context()
    page = browser.new_page()

    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_selector("a.frame")

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")

    movies_data = soup.find_all(class_="image")

    movies = []
    for img in movies_data:
        new_movie = {"name":img["alt"], "image":img["src"]}
        movies.append(new_movie)

    return movies

def url_builder(query, url, filters):
    for key, value in query.items():
        if value == "Cualquiera":
            options = filters[key]
            query[key] = choice(options)

    new_url = f"{url}/year/{query["year"]}/genre/{query["genre"]}"
    return new_url

def scrape_data_main(query, data):
    new_query = json.loads(query)
    server_data = json.loads(data)

    letterboxd_url = url_builder(new_query, server_data["url"], server_data["filters"])
    pattern = r"(?<=\s)\d+(?=\s)"
    page_limit = server_data["pagelimit"]

    with sync_playwright() as p:
        process_browser = p.chromium.launch(headless=True)

        page_count = get_page_count(page_limit, pattern, process_browser, letterboxd_url)

        movies_payload = []

        for p in range(1, (page_count + 1)):
            page_url = f"{letterboxd_url}/page/{p}/"
            page_data = get_movies(page_url, process_browser)
            movies_payload.extend(page_data)
    
    return choice(movies_payload)

if __name__ == "__main__":
    data = scrape_data_main(sys.argv[1], sys.argv[2])
    print(json.dumps(data))