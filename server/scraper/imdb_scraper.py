import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json
import sys
import re
import math
from random import choice

def get_movies_from_page(url):
    res = requests.get(url, headers=search_headers)
    page_data = res.json()["data"]["advancedTitleSearch"]

    movies_payload = {}

    if not page_data['pageInfo']['hasPreviousPage']:
        movies_payload['search-data'] = {
            'count': page_data['total'],
            'next-cursor': page_data['pageInfo']['endCursor']
        }
    elif page_data['pageInfo']['hasNextPage']:
        movies_payload['search-data'] = {
            'next-cursor': page_data['pageInfo']['endCursor']
        }
    
    movies_payload['movies'] = []

    for m in page_data['edges']:
        m_data = m['node']['title']

        current_movie = {
            'id': m_data['id'],
            'title': m_data['titleText']['text'],
            'type': m_data['titleType']['text'],
            'image': m_data['primaryImage']['url'],
            'year': m_data['releaseYear']['year'],
            'rating': m_data['ratingsSummary']['aggregateRating'],
            'genres': [g['genre']['text'] for g in m_data['titleGenres']['genres']],
            'plot': m_data['plot']['plotText']['plainText']
        }

        movies_payload['movies'].append(current_movie)
    
    return movies_payload

def scrape_data_main(query):
    new_query = json.loads(query)

    movie_list = get_movies_from_page('https://caching.graphql.imdb.com/?operationName=AdvancedTitleSearch&variables={"first"%3A50%2C"genreConstraint"%3A{"allGenreIds"%3A["Film-Noir"]%2C"excludeGenreIds"%3A["Talk-Show"%2C"Reality-TV"%2C"News"%2C"Game-Show"%2C"Documentary"%2C"Short"]}%2C"locale"%3A"en-US"%2C"sortBy"%3A"POPULARITY"%2C"sortOrder"%3A"ASC"}&extensions={"persistedQuery"%3A{"sha256Hash"%3A"60a7b8470b01671336ffa535b21a0a6cdaf50267fa2ab55b3e3772578a8c1f00"%2C"version"%3A1}}')

    return {"name": str(new_query), "img": str(movie_list)}

if __name__ == "__main__":

    search_headers = {
    'Content-type':'application/json', 
    'Accept':'application/json'
    }

    data = scrape_data_main(sys.argv[1])
    print(json.dumps(data))

