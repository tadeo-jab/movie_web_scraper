import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json
import sys
import re
import math
from random import choice as random_choice
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, unquote, quote


def get_credits(name):
    testurl_1 = unquote('https://caching.graphql.imdb.com/?operationName=FindPageSearch&variables={"after"%3A"eyJlc1Rva2VuIjpbIjg2OTAuNDk0Iiwibm0wNTUzMDQ3Il0sImZpbHRlciI6IntcImluY2x1ZGVBZHVsdFwiOmZhbHNlLFwiaXNFeGFjdE1hdGNoXCI6ZmFsc2UsXCJzZWFyY2hUZXJtXCI6XCJtYXJ0aW4gc2NvXCIsXCJ0eXBlXCI6W1wiTkFNRVwiXX0ifQ%3D%3D"%2C"includeAdult"%3Afalse%2C"isExactMatch"%3Afalse%2C"locale"%3A"es-MX"%2C"numResults"%3A25%2C"searchTerm"%3A"martin sco"%2C"skipHasExact"%3Atrue%2C"typeFilter"%3A"NAME"}&extensions={"persistedQuery"%3A{"sha256Hash"%3A"038ff5315025edc006d874aa81178b17335fcae8fecc25bf7c2ce3f1b8085b60"%2C"version"%3A1}}')
    testurl_2 = 'https://caching.graphql.imdb.com/?operationName=FindPageSearch&variables={"after":"eyJlc1Rva2VuIjpbIjg2OTAuNDk0Iiwibm0wNTUzMDQ3Il0sImZpbHRlciI6IntcImluY2x1ZGVBZHVsdFwiOmZhbHNlLFwiaXNFeGFjdE1hdGNoXCI6ZmFsc2UsXCJzZWFyY2hUZXJtXCI6XCJtYXJ0aW4gc2NvXCIsXCJ0eXBlXCI6W1wiTkFNRVwiXX0ifQ==","includeAdult":false,"isExactMatch":false,"locale":"es-MX","numResults":25,"searchTerm":"martin sco","skipHasExact":true,"typeFilter":"NAME"}&extensions={"persistedQuery":{"sha256Hash":"038ff5315025edc006d874aa81178b17335fcae8fecc25bf7c2ce3f1b8085b60","version":1}}'
    testurl_3 = f'https://caching.graphql.imdb.com/?operationName=FindPageSearch&variables={{"first":1,"includeAdult":false,"isExactMatch":false,"locale":"en-US","numResults":1,"searchTerm":"{name}","skipHasExact":true,"typeFilter":"NAME"}}&extensions={{"persistedQuery":{{"sha256Hash":"038ff5315025edc006d874aa81178b17335fcae8fecc25bf7c2ce3f1b8085b60","version":1}}}}'


    res = requests.get(testurl_3, headers=search_data['headers'])
    search_result = res.json()['data']['results']['edges']

    if search_result:
        credit_id = search_result[0]['node']['entity']['id']
        return {'nameId': credit_id}
    else:
        return {}
    

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
    #Actually, it can.
    if (var_data.get('credits', None)) != None:
        url_variables.update({
            'titleCreditsConstraint':{
                'allCredits': var_data['credits'],
                'excludeCredits': []
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

    

def get_movies(url):
    res = requests.get(url, headers=search_data['headers'])

    page_data = res.json()["data"]["advancedTitleSearch"]
    movies_payload = {'movies':[]}

    for m in page_data['edges']:
        m_data = m['node']['title']

        current_movie = {
            'id': m_data.get('id', {}),
            'title': m_data.get('titleText', {}).get('text', {}) if(m_data.get('titleText', {}) != None) else None,
            'type': m_data.get('titleType', {}).get('text', {}) if(m_data.get('titleType', {}) != None) else None,
            'image': m_data.get('primaryImage', {}).get('url', {}) if(m_data.get('primaryImage', {}) != None) else None,
            'year': m_data.get('releaseYear', {}).get('year', {}) if(m_data.get('releaseYear', {}) != None) else None,
            'rating': m_data.get('ratingsSummary', {}).get('aggregateRating', {}) if(m_data.get('ratingsSummary', {}) != None) else None,
            'genres': [g['genre']['text'] for g in m_data['titleGenres']['genres']] if(m_data.get('titleGenres', {}) != None) else None,
            'plot': m_data.get('plot', {}).get('plotText', {}).get('plainText', {}) if((m_data.get('plot', {}) != None) and (m_data.get('plot', {}).get('plotText', {}) != None)) else None
        }

        movies_payload['movies'].append(current_movie)
    
    return movies_payload

def scrape_data_main(query):
    new_query = json.loads(query)
    url_filters = new_query.copy()
    
    credit_ids = []
    if (new_query.get('actor', None) != None):
        credit_ids.append(get_credits(new_query['actor']))
        del url_filters['actor']
    
    if (new_query.get('director', None) != None):
        credit_ids.append(get_credits(new_query['director']))
        del url_filters['director']
    
    if credit_ids:
        url_filters.update({'credits': credit_ids})

    sort_type = random_choice(search_data['sort_options'])
    sort_order = random_choice(search_data['order_options'])

    url_filters.update({
        'sort': sort_type,
        'order': sort_order,
        'load_limit': search_data['count'],
        'excluded': search_data['excluded_genres']
    })

    if new_query.get('animated', None) != None:
        del url_filters['animated']
        if (new_query['animated']) and (new_query.get('genres', None) != None):
            url_filters['genres'].append('Animation')
        elif (new_query['animated']) and (new_query.get('genres', None) == None):
            url_filters.update({'genres': ['Animation']})
        elif not new_query['animated']:
            url_filters['excluded'].append('Animation')

    try:
        search_url = url_builder(url_filters)
        #movie_list = get_movies_from_page('https://caching.graphql.imdb.com/?operationName=AdvancedTitleSearch&variables=%7B%22certificateConstraint%22%3A%7B%22anyRegionCertificateRatings%22%3A%5B%7B%22rating%22%3A%22R%22%2C%22region%22%3A%22US%22%7D%5D%2C%22excludeRegionCertificateRatings%22%3A%5B%5D%7D%2C%22first%22%3A50%2C%22genreConstraint%22%3A%7B%22allGenreIds%22%3A%5B%22Crime%22%2C%22Thriller%22%5D%2C%22excludeGenreIds%22%3A%5B%22Talk-Show%22%2C%22Reality-TV%22%2C%22News%22%2C%22Game-Show%22%2C%22Documentary%22%2C%22Short%22%5D%7D%2C%22locale%22%3A%22en-US%22%2C%22originCountryConstraint%22%3A%7B%22anyPrimaryCountries%22%3A%5B%22US%22%5D%7D%2C%22releaseDateConstraint%22%3A%7B%22releaseDateRange%22%3A%7B%22end%22%3A%222024-12-31%22%2C%22start%22%3A%221980-01-01%22%7D%7D%2C%22runtimeConstraint%22%3A%7B%22runtimeRangeMinutes%22%3A%7B%22max%22%3A180%2C%22min%22%3A1%7D%7D%2C%22sortBy%22%3A%22USER_RATING%22%2C%22sortOrder%22%3A%22DESC%22%2C%22titleCreditsConstraint%22%3A%7B%22allCredits%22%3A%5B%7B%22nameId%22%3A%22nm0000233%22%7D%2C%7B%22nameId%22%3A%22nm0000168%22%7D%5D%2C%22excludeCredits%22%3A%5B%5D%7D%2C%22titleTypeConstraint%22%3A%7B%22anyTitleTypeIds%22%3A%5B%22movie%22%5D%2C%22excludeTitleTypeIds%22%3A%5B%5D%7D%2C%22userRatingsConstraint%22%3A%7B%22aggregateRatingRange%22%3A%7B%22max%22%3A9.9%2C%22min%22%3A5%7D%7D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22sha256Hash%22%3A%2260a7b8470b01671336ffa535b21a0a6cdaf50267fa2ab55b3e3772578a8c1f00%22%2C%22version%22%3A1%7D%7D')

        #movie_list = get_movies_from_page(search_url)

        #with_actors = 'https://caching.graphql.imdb.com/?operationName=AdvancedTitleSearch&variables=%7B%22certificateConstraint%22%3A%7B%22anyRegionCertificateRatings%22%3A%5B%7B%22rating%22%3A%22R%22%2C%22region%22%3A%22US%22%7D%5D%2C%22excludeRegionCertificateRatings%22%3A%5B%5D%7D%2C%22first%22%3A50%2C%22genreConstraint%22%3A%7B%22allGenreIds%22%3A%5B%22Crime%22%2C%22Thriller%22%5D%2C%22excludeGenreIds%22%3A%5B%22Talk-Show%22%2C%22Reality-TV%22%2C%22News%22%2C%22Game-Show%22%2C%22Documentary%22%2C%22Short%22%5D%7D%2C%22locale%22%3A%22en-US%22%2C%22originCountryConstraint%22%3A%7B%22anyPrimaryCountries%22%3A%5B%22US%22%5D%7D%2C%22releaseDateConstraint%22%3A%7B%22releaseDateRange%22%3A%7B%22end%22%3A%222024-12-31%22%2C%22start%22%3A%221980-01-01%22%7D%7D%2C%22runtimeConstraint%22%3A%7B%22runtimeRangeMinutes%22%3A%7B%22max%22%3A180%2C%22min%22%3A1%7D%7D%2C%22sortBy%22%3A%22USER_RATING%22%2C%22sortOrder%22%3A%22DESC%22%2C%22titleCreditsConstraint%22%3A%7B%22allCredits%22%3A%5B%7B%22nameId%22%3A%22nm0000233%22%7D%2C%7B%22nameId%22%3A%22nm0000168%22%7D%5D%2C%22excludeCredits%22%3A%5B%5D%7D%2C%22titleTypeConstraint%22%3A%7B%22anyTitleTypeIds%22%3A%5B%22movie%22%5D%2C%22excludeTitleTypeIds%22%3A%5B%5D%7D%2C%22userRatingsConstraint%22%3A%7B%22aggregateRatingRange%22%3A%7B%22max%22%3A9.9%2C%22min%22%3A5%7D%7D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22sha256Hash%22%3A%2260a7b8470b01671336ffa535b21a0a6cdaf50267fa2ab55b3e3772578a8c1f00%22%2C%22version%22%3A1%7D%7D'
        #no_actors = 'https://caching.graphql.imdb.com/?operationName=AdvancedTitleSearch&variables=%7B%22certificateConstraint%22%3A%7B%22anyRegionCertificateRatings%22%3A%5B%7B%22rating%22%3A%22R%22%2C%22region%22%3A%22US%22%7D%5D%2C%22excludeRegionCertificateRatings%22%3A%5B%5D%7D%2C%22first%22%3A50%2C%22genreConstraint%22%3A%7B%22allGenreIds%22%3A%5B%22Crime%22%2C%22Thriller%22%5D%2C%22excludeGenreIds%22%3A%5B%22Talk-Show%22%2C%22Reality-TV%22%2C%22News%22%2C%22Game-Show%22%2C%22Documentary%22%2C%22Short%22%5D%7D%2C%22locale%22%3A%22en-US%22%2C%22originCountryConstraint%22%3A%7B%22anyPrimaryCountries%22%3A%5B%22US%22%5D%7D%2C%22releaseDateConstraint%22%3A%7B%22releaseDateRange%22%3A%7B%22end%22%3A%222024-12-31%22%2C%22start%22%3A%221980-01-01%22%7D%7D%2C%22runtimeConstraint%22%3A%7B%22runtimeRangeMinutes%22%3A%7B%22max%22%3A180%2C%22min%22%3A1%7D%7D%2C%22sortBy%22%3A%22USER_RATING%22%2C%22sortOrder%22%3A%22DESC%22%2C%22titleTypeConstraint%22%3A%7B%22anyTitleTypeIds%22%3A%5B%22movie%22%5D%2C%22excludeTitleTypeIds%22%3A%5B%5D%7D%2C%22userRatingsConstraint%22%3A%7B%22aggregateRatingRange%22%3A%7B%22max%22%3A9.9%2C%22min%22%3A5%7D%7D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22sha256Hash%22%3A%2260a7b8470b01671336ffa535b21a0a6cdaf50267fa2ab55b3e3772578a8c1f00%22%2C%22version%22%3A1%7D%7D'

        #mine_list = get_movies(search_url)
        #site_list_no = get_movies(no_actors)
        #site_list_yes = get_movies(with_actors)
        #return {'mine': search_url, 'site': no_actors}
        #return {'mine': mine_list, 'site':site_list_yes}
        #return movie_list

        movie_list = get_movies(search_url)

        return {'data': movie_list}
    except Exception as err:
        return {'err': str((err))}

def testee(fff):
    
    return {"data": str(fff)}

if __name__ == "__main__":
    utils = json.loads(sys.argv[2])
    search_data = utils['search_utils']

    data = scrape_data_main(sys.argv[1])
    print(json.dumps(data))

