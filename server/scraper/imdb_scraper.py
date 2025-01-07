import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json
import sys
import re
import math
from random import choice as random_choice
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, unquote, quote

def get_credits(lst):
    return [
    {
        "nameId": "nm0000233"
    },
    {
        "nameId": "nm0000168"
    }
]

def url_builder(var_data):
    url_data = utils['url']

    url_variables = url_data['variables']
    url_variables['first'] = var_data['load_limit']
    url_variables['sortBy'] = var_data['sort']
    url_variables['sortOrder'] = var_data['order']

    #Can be empty - And deleted
    if (var_data.get('parental', None)) != None:
        url_variables.update({
            'certificateConstraint':{
                'anyRegionCertificateRatings': [{'rating': var_data['parental'], 'region': 'US'}],
                'excludeRegionCertificateRatings': []
            }
        })

    #Can be empty and deleted
    if ((var_data.get('genres', None)) != None) or ((var_data.get('excluded', None)) != None):
        url_variables.update({
            'genreConstraint':{
                "allGenreIds": var_data.get('genres', []),
                "excludeGenreIds": var_data.get('excluded', [])
            }
        })
    
    #Can be Empty - And deleted?
    if (var_data.get('country', None)) != None:
        url_variables.update({
            'originCountryConstraint':{
                'anyPrimaryCountries': [var_data['country']]
            }
        })
    
    #Can be Empty and deleted
    if (var_data.get('date', None)) != None:
        url_variables.update({
            'releaseDateConstraint':{
                'releaseDateRange': var_data['date']
            }
        })

    #Can be Empty and Deleted
    if (var_data.get('runtime', None)) != None:
        url_variables.update({
            'runtimeConstraint':{
                'runtimeRangeMinutes': var_data['runtime']
            }
        })

    #Can be Empty and Deleted
    if (var_data.get('rating', None)) != None:
        url_variables.update({
            'userRatingsConstraint':{
                'aggregateRatingRange': var_data['rating']
            }
        })

    #Can be empty and deleted
    if (var_data.get('type', None)) != None:
        url_variables.update({
            'titleTypeConstraint':{
                'anyTitleTypeIds': [var_data['type']],
                'excludeTitleTypeIds': []
            }
        })
    
    #Can't be empty nor deleted
    if (var_data.get('people', None)) != None:
        url_variables.update({
            'titleCreditsConstraint':{
                'allCredits': [{"nameId":"nm0000233"}],
                'excludeCredits': [{"nameId":"nm0000168"}]
            }
        })
    
    query_params = {
    "operationName": url_data['operation_name'],
    "variables": json.dumps(url_variables),
    "extensions": json.dumps(url_data['extensions'])
    }

    encoded_params = urlencode({k: v if k != 'variables' else v for k, v in query_params.items()})

    new_url = f'{url_data['base_url']}?{encoded_params}'

    unquoteddd = unquote(new_url)

    final_test = re.sub("\+", "", unquoteddd)
    return final_test

    

def get_movies_from_page(url):

    #res = requests.get(unquote(url), headers=search_data['headers'])
    res = requests.get(url, headers=search_data['headers'])

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

    credit_ids = None
    if (new_query['actor'] != None) and (new_query['director'] != None):
        credit_ids = get_credits([])

    sort_type = random_choice(search_data['sort_options'])
    sort_order = random_choice(search_data['order_options'])

    new_query.update({
        "people": credit_ids,
        'sort': sort_type,
        'order': sort_order,
        'load_limit': search_data['count'],
        'excluded': search_data['excluded_genres']
    })

    try:
        search_url = url_builder(new_query)
        #movie_list = get_movies_from_page('https://caching.graphql.imdb.com/?operationName=AdvancedTitleSearch&variables=%7B%22certificateConstraint%22%3A%7B%22anyRegionCertificateRatings%22%3A%5B%7B%22rating%22%3A%22R%22%2C%22region%22%3A%22US%22%7D%5D%2C%22excludeRegionCertificateRatings%22%3A%5B%5D%7D%2C%22first%22%3A50%2C%22genreConstraint%22%3A%7B%22allGenreIds%22%3A%5B%22Crime%22%2C%22Thriller%22%5D%2C%22excludeGenreIds%22%3A%5B%22Talk-Show%22%2C%22Reality-TV%22%2C%22News%22%2C%22Game-Show%22%2C%22Documentary%22%2C%22Short%22%5D%7D%2C%22locale%22%3A%22en-US%22%2C%22originCountryConstraint%22%3A%7B%22anyPrimaryCountries%22%3A%5B%22US%22%5D%7D%2C%22releaseDateConstraint%22%3A%7B%22releaseDateRange%22%3A%7B%22end%22%3A%222024-12-31%22%2C%22start%22%3A%221980-01-01%22%7D%7D%2C%22runtimeConstraint%22%3A%7B%22runtimeRangeMinutes%22%3A%7B%22max%22%3A180%2C%22min%22%3A1%7D%7D%2C%22sortBy%22%3A%22USER_RATING%22%2C%22sortOrder%22%3A%22DESC%22%2C%22titleCreditsConstraint%22%3A%7B%22allCredits%22%3A%5B%7B%22nameId%22%3A%22nm0000233%22%7D%2C%7B%22nameId%22%3A%22nm0000168%22%7D%5D%2C%22excludeCredits%22%3A%5B%5D%7D%2C%22titleTypeConstraint%22%3A%7B%22anyTitleTypeIds%22%3A%5B%22movie%22%5D%2C%22excludeTitleTypeIds%22%3A%5B%5D%7D%2C%22userRatingsConstraint%22%3A%7B%22aggregateRatingRange%22%3A%7B%22max%22%3A9.9%2C%22min%22%3A5%7D%7D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22sha256Hash%22%3A%2260a7b8470b01671336ffa535b21a0a6cdaf50267fa2ab55b3e3772578a8c1f00%22%2C%22version%22%3A1%7D%7D')

        movie_list = get_movies_from_page(search_url)


        #return {'mine': search_url, 'site': unquote('https://caching.graphql.imdb.com/?operationName=AdvancedTitleSearch&variables=%7B%22certificateConstraint%22%3A%7B%22anyRegionCertificateRatings%22%3A%5B%7B%22rating%22%3A%22R%22%2C%22region%22%3A%22US%22%7D%5D%2C%22excludeRegionCertificateRatings%22%3A%5B%5D%7D%2C%22first%22%3A50%2C%22genreConstraint%22%3A%7B%22allGenreIds%22%3A%5B%22Crime%22%2C%22Thriller%22%5D%2C%22excludeGenreIds%22%3A%5B%22Talk-Show%22%2C%22Reality-TV%22%2C%22News%22%2C%22Game-Show%22%2C%22Documentary%22%2C%22Short%22%5D%7D%2C%22locale%22%3A%22en-US%22%2C%22originCountryConstraint%22%3A%7B%22anyPrimaryCountries%22%3A%5B%22US%22%5D%7D%2C%22releaseDateConstraint%22%3A%7B%22releaseDateRange%22%3A%7B%22end%22%3A%222024-12-31%22%2C%22start%22%3A%221980-01-01%22%7D%7D%2C%22runtimeConstraint%22%3A%7B%22runtimeRangeMinutes%22%3A%7B%22max%22%3A180%2C%22min%22%3A1%7D%7D%2C%22sortBy%22%3A%22USER_RATING%22%2C%22sortOrder%22%3A%22DESC%22%2C%22titleCreditsConstraint%22%3A%7B%22allCredits%22%3A%5B%7B%22nameId%22%3A%22nm0000233%22%7D%2C%7B%22nameId%22%3A%22nm0000168%22%7D%5D%2C%22excludeCredits%22%3A%5B%5D%7D%2C%22titleTypeConstraint%22%3A%7B%22anyTitleTypeIds%22%3A%5B%22movie%22%5D%2C%22excludeTitleTypeIds%22%3A%5B%5D%7D%2C%22userRatingsConstraint%22%3A%7B%22aggregateRatingRange%22%3A%7B%22max%22%3A9.9%2C%22min%22%3A5%7D%7D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22sha256Hash%22%3A%2260a7b8470b01671336ffa535b21a0a6cdaf50267fa2ab55b3e3772578a8c1f00%22%2C%22version%22%3A1%7D%7D')}

        return movie_list
    except Exception as err:
        return {'err': str(type(err))}

def testee(fff):
    
    return {"data": str(fff)}

if __name__ == "__main__":
    utils = json.loads(sys.argv[2])
    search_data = utils['search_utils']

    data = scrape_data_main(sys.argv[1])
    print(json.dumps(data))

