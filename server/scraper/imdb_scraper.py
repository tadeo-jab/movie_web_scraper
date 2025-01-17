import requests
from bs4 import BeautifulSoup
import json
import sys
import re
from random import choice as random_choice, sample as random_sample
from urllib.parse import urlencode, unquote



#The program's goal is to get a list of movies from IMDb's website, taking multiple filters into account.

#Since the target website is loaded dynamically, the data isn't scraped directly from a static HTML file.

#Instead, the strategy of this scraper is to simulate the API request performed by the website, 
#and receiving the data directly, like the front-end would.

#A much faster and cleaner process than using browser simulators like Playwright.


def url_builder(var_data):
    url_data = utils['url']

    url_variables = url_data['variables']
    url_variables['first'] = var_data['load_limit']
    url_variables['sortBy'] = var_data['sort']
    url_variables['sortOrder'] = var_data['order']

    #The URL dictionary is updated according to the filters passed by the front-end.

    if ('parental' in var_data):
        url_variables.update({
            'certificateConstraint':{
                'anyRegionCertificateRatings': [{'rating': var_data['parental'], 'region': 'US'}],
                'excludeRegionCertificateRatings': []
            }
        })

    if ('genres' in var_data) or ('excluded' in var_data):
        url_variables.update({
            'genreConstraint':{
                "allGenreIds": var_data.get('genres', []),
                "excludeGenreIds": var_data.get('excluded', [])
            }
        })
    
    if ('country' in var_data):
        url_variables.update({
            'originCountryConstraint':{
                'anyPrimaryCountries': [var_data['country']]
            }
        })
    
    if ('date' in var_data):
        url_variables.update({
            'releaseDateConstraint':{
                'releaseDateRange': var_data['date']
            }
        })

    if ('runtime' in var_data):
        url_variables.update({
            'runtimeConstraint':{
                'runtimeRangeMinutes': {'min': var_data['runtime']['min'], 'max': var_data['runtime']['max']}
            }
        })

    if ('rating' in var_data) or ('popularity' in var_data):
        url_variables.update({ 
            'userRatingsConstraint':{
                **({'aggregateRatingRange': {'min': var_data['rating']['min'], 'max': var_data['rating']['max']}} if ('rating' in var_data) else {}),
                **({'ratingsCountRange': {'min': var_data['popularity']['min'], 'max': var_data['popularity']['max']}} if ('popularity' in var_data) else {}),
            }})
            
    if ('type' in var_data):
        url_variables.update({
            'titleTypeConstraint':{
                'anyTitleTypeIds': [var_data['type']],
                'excludeTitleTypeIds': []
            }
        })
    
    if ('credits' in var_data):
        url_variables.update({
            'titleCreditsConstraint':{
                'allCredits': var_data['credits'],
                'excludeCredits': []
            }
        })

    if ('company' in var_data):
        url_variables.update({
            'creditedCompanyConstraint':{
                "anyCompanyIds": var_data['company'],
                "excludeCompanyIds": []
            }
        })

    if ('awards' in var_data):
        url_variables.update({
            'awardConstraint':{
                "allEventNominations": var_data['awards']
            }
        })

    
    #The dictionary is then converted into a functional URL

    query_params = {
    "operationName": url_data['operation_name'],
    "variables": json.dumps(url_variables),
    "extensions": json.dumps(url_data['extensions'])
    }

    encoded_params = urlencode({k: v if k != 'variables' else v for k, v in query_params.items()})

    new_url = f'{url_data['base_url']}?{encoded_params}'

    unquoted = unquote(new_url)

    final_url = re.sub("\+", "", unquoted)
    return final_url

    
#Receives the data from the API, and returns only the necessary data.

def get_movies(url):
    res = requests.get(url, headers=search_data['headers'])

    page_data = res.json()["data"]["advancedTitleSearch"]
    movies_payload = []

    for m in page_data['edges']:
        m_data = m['node']['title']

        current_movie = {
            'id': m_data.get('id', {}),
            'title': m_data.get('titleText', {}).get('text', {}) if('titleText' in m_data) else None,
            'type': m_data.get('titleType', {}).get('text', {}) if('titleType' in m_data) else None,
            'image': m_data.get('primaryImage', {}).get('url', {}) if('primaryImage' in m_data) else None,
            'year': m_data.get('releaseYear', {}).get('year', {}) if('releaseYear' in m_data) else None,
            'rating': m_data.get('ratingsSummary', {}).get('aggregateRating', {}) if('ratingsSummary' in m_data) else None,
            'genres': [g['genre']['text'] for g in m_data['titleGenres']['genres']] if('titleGenres' in m_data) else None,
            'plot': m_data.get('plot', {}).get('plotText', {}).get('plainText', {}) if(('plot' in m_data) and (m_data.get('plot', {}).get('plotText', {}) != None)) else None
        }

        movies_payload.append(current_movie)
    
    return movies_payload


#To search by actor, a different URL is scraped, using the same procedure.
#Mimics a celebrity search performed by a user, and reads only the first result (The most popular one). 

def get_credits(name):
    c_utils = utils['url']['credit_search']

    base_url = unquote(c_utils['base_url'])
    credit_url = re.sub(c_utils['key'], name, base_url)

    res = requests.get(credit_url, headers=search_data['headers'])
    search_result = res.json()['data']['results']['edges']

    if search_result:
        credit_id = search_result[0]['node']['entity']['id']
        return {'nameId': credit_id}
    else:
        return {}


def scrape_data_main(query):

    #Some query params received from the front-end must be modified before being included in the URL

    new_query = json.loads(query)
    url_filters = new_query.copy()
    
    credit_ids = []
    if ('actor' in new_query):
        credit_ids.append(get_credits(new_query['actor']))
        del url_filters['actor']
    
    if ('director' in new_query):
        credit_ids.append(get_credits(new_query['director']))
        del url_filters['director']
    
    if credit_ids:
        url_filters.update({'credits': credit_ids})

    #For an extra random factor, an arbitrary sorting option and order is chosen.

    sort_type = random_choice(search_data['sort_options'])
    sort_order = random_choice(search_data['order_options'])

    url_filters.update({
        'sort': sort_type,
        'order': sort_order,
        'load_limit': search_data['count']
    })

    if ('excluded' not in new_query):
        url_filters.update({
            'excluded': search_data['defaults'].get('excluded')
        })

    if ('popularity' not in new_query):
        url_filters.update({
            'popularity': search_data['defaults'].get('popularity')
        })

    #Animation is a genre, so it must either be included as one or as part of the blacklisted ones.

    if ('animated' in new_query):
        del url_filters['animated']
        if (new_query['animated']) and ('genres' in new_query):
            url_filters['genres'].append('Animation')
        elif (new_query['animated']) and ('genres' not in new_query):
            url_filters.update({'genres': ['Animation']})
        elif not new_query['animated']:
            url_filters['excluded'].append('Animation')

    try:
        search_url = url_builder(url_filters)
        movie_list = get_movies(search_url)

        #Of the 100 movies, only 7 are selected at random, and sent to the front-end.

        if len(movie_list) > search_data['selection_limit']:
            selected_movies = random_sample(movie_list, search_data['selection_limit'])
        else:
            selected_movies = movie_list

        return {'data': selected_movies}
    except Exception as err:
        return {'err': str((err))}


if __name__ == "__main__":
    utils = json.loads(sys.argv[2])
    search_data = utils['search_utils']

    data = scrape_data_main(sys.argv[1])
    print(json.dumps(data))

