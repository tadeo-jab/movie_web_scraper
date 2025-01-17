import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json
import sys
import re
import math
from random import choice as random_choice, sample as random_sample
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, unquote, quote


def get_credits(name):
    credit_url = f'https://caching.graphql.imdb.com/?operationName=FindPageSearch&variables={{"first":1,"includeAdult":false,"isExactMatch":false,"locale":"en-US","numResults":1,"searchTerm":"{name}","skipHasExact":true,"typeFilter":"NAME"}}&extensions={{"persistedQuery":{{"sha256Hash":"038ff5315025edc006d874aa81178b17335fcae8fecc25bf7c2ce3f1b8085b60","version":1}}}}'

    res = requests.get(credit_url, headers=search_data['headers'])
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
                'runtimeRangeMinutes': {'min': var_data['runtime']['min'], 'max': var_data['runtime']['max']}
            }
        })

    #Can be Empty and Deleted
    if ((var_data.get('rating', None)) != None) or ((var_data.get('popularity', None)) != None):
        url_variables.update({ 
            'userRatingsConstraint':{
                **({'aggregateRatingRange': {'min': var_data['rating']['min'], 'max': var_data['rating']['max']}} if ((var_data.get('rating', None)) != None) else {}),
                **({'ratingsCountRange': {'min': var_data['popularity']['min'], 'max': var_data['popularity']['max']}} if ((var_data.get('popularity', None)) != None) else {}),
            }})
            
        

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

    if (var_data.get('company', None)) != None:
        url_variables.update({
            'creditedCompanyConstraint':{
                "anyCompanyIds": var_data['company'],
                "excludeCompanyIds": []
            }
        })

    if (var_data.get('awards', None)) != None:
        url_variables.update({
            'awardConstraint':{
                "allEventNominations": var_data['awards']
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
    movies_payload = []

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

        movies_payload.append(current_movie)
    
    return movies_payload

def url_test(url):
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    variables = json.loads(query_params['variables'][0])
    return variables

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
        'load_limit': search_data['count']
    })

    if 'excluded' not in new_query:
        url_filters.update({
            'excluded': search_data['defaults'].get('excluded')
        })

    if 'popularity' not in new_query:
        url_filters.update({
            'popularity': search_data['defaults'].get('popularity')
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

        search_url = url_builder(url_filters)
        movie_list = get_movies(search_url)

        #popularity_url = 'https://caching.graphql.imdb.com/?operationName=AdvancedTitleSearch&variables={"awardConstraint"%3A{"allEventNominations"%3A[{"eventId"%3A"ev0000003"}%2C{"eventId"%3A"ev0000003"%2C"winnerFilter"%3A"WINNER_ONLY"}]%2C"excludeEventNominations"%3A[]}%2C"creditedCompanyConstraint"%3A{"anyCompanyIds"%3A["co0000756"%2C"co0176225"%2C"co0201557"%2C"co0017497"%2C"co0008970"%2C"co0017902"%2C"co0098836"%2C"co0059516"%2C"co0092035"%2C"co0049348"]%2C"excludeCompanyIds"%3A[]}%2C"first"%3A50%2C"locale"%3A"en-US"%2C"rankedTitleListConstraint"%3A{"allRankedTitleLists"%3A[{"rankRange"%3A{"max"%3A5000%2C"min"%3A1}%2C"rankedTitleListType"%3A"TITLE_METER"}]%2C"excludeRankedTitleLists"%3A[]}%2C"sortBy"%3A"POPULARITY"%2C"sortOrder"%3A"ASC"}&extensions={"persistedQuery"%3A{"sha256Hash"%3A"60a7b8470b01671336ffa535b21a0a6cdaf50267fa2ab55b3e3772578a8c1f00"%2C"version"%3A1}}'
        #company_url = 'https://caching.graphql.imdb.com/?operationName=AdvancedTitleSearch&variables={"certificateConstraint"%3A{"anyRegionCertificateRatings"%3A[{"rating"%3A"R"%2C"region"%3A"US"}]%2C"excludeRegionCertificateRatings"%3A[]}%2C"creditedCompanyConstraint"%3A{"anyCompanyIds"%3A["co0023400"]%2C"excludeCompanyIds"%3A[]}%2C"first"%3A50%2C"genreConstraint"%3A{"allGenreIds"%3A["Crime"%2C"Thriller"]%2C"excludeGenreIds"%3A["Talk-Show"%2C"Reality-TV"%2C"News"%2C"Game-Show"%2C"Documentary"%2C"Short"]}%2C"locale"%3A"en-US"%2C"originCountryConstraint"%3A{"anyPrimaryCountries"%3A["US"]}%2C"releaseDateConstraint"%3A{"releaseDateRange"%3A{"end"%3A"2024-12-31"%2C"start"%3A"1980-01-01"}}%2C"runtimeConstraint"%3A{"runtimeRangeMinutes"%3A{"max"%3A180%2C"min"%3A1}}%2C"sortBy"%3A"USER_RATING"%2C"sortOrder"%3A"DESC"%2C"titleCreditsConstraint"%3A{"allCredits"%3A[{"nameId"%3A"nm0000233"}%2C{"nameId"%3A"nm0000168"}]}%2C"titleTypeConstraint"%3A{"anyTitleTypeIds"%3A["movie"]%2C"excludeTitleTypeIds"%3A[]}%2C"userRatingsConstraint"%3A{"aggregateRatingRange"%3A{"max"%3A9.9%2C"min"%3A5}}}&extensions={"persistedQuery"%3A{"sha256Hash"%3A"60a7b8470b01671336ffa535b21a0a6cdaf50267fa2ab55b3e3772578a8c1f00"%2C"version"%3A1}}'
        #award_url = 'https://caching.graphql.imdb.com/?operationName=AdvancedTitleSearch&variables={"awardConstraint"%3A{"allEventNominations"%3A[{"eventId"%3A"ev0000003"%2C"searchAwardCategoryId"%3A"bestDirector"%2C"winnerFilter"%3A"WINNER_ONLY"}%2C{"eventId"%3A"ev0000003"%2C"winnerFilter"%3A"WINNER_ONLY"}%2C{"eventId"%3A"ev0000003"%2C"searchAwardCategoryId"%3A"bestDirector"}%2C{"eventId"%3A"ev0000003"}]}%2C"certificateConstraint"%3A{"anyRegionCertificateRatings"%3A[{"rating"%3A"R"%2C"region"%3A"US"}]%2C"excludeRegionCertificateRatings"%3A[]}%2C"creditedCompanyConstraint"%3A{"anyCompanyIds"%3A["co0023400"]%2C"excludeCompanyIds"%3A[]}%2C"first"%3A50%2C"genreConstraint"%3A{"allGenreIds"%3A["Crime"%2C"Thriller"]%2C"excludeGenreIds"%3A["Talk-Show"%2C"Reality-TV"%2C"News"%2C"Game-Show"%2C"Documentary"%2C"Short"]}%2C"locale"%3A"en-US"%2C"originCountryConstraint"%3A{"anyPrimaryCountries"%3A["US"]}%2C"releaseDateConstraint"%3A{"releaseDateRange"%3A{"end"%3A"2024-12-31"%2C"start"%3A"1980-01-01"}}%2C"runtimeConstraint"%3A{"runtimeRangeMinutes"%3A{"max"%3A180%2C"min"%3A1}}%2C"sortBy"%3A"USER_RATING"%2C"sortOrder"%3A"DESC"%2C"titleCreditsConstraint"%3A{"allCredits"%3A[{"nameId"%3A"nm0000233"}%2C{"nameId"%3A"nm0000168"}]}%2C"titleTypeConstraint"%3A{"anyTitleTypeIds"%3A["movie"]%2C"excludeTitleTypeIds"%3A[]}%2C"userRatingsConstraint"%3A{"aggregateRatingRange"%3A{"max"%3A9.9%2C"min"%3A5}}}&extensions={"persistedQuery"%3A{"sha256Hash"%3A"60a7b8470b01671336ffa535b21a0a6cdaf50267fa2ab55b3e3772578a8c1f00"%2C"version"%3A1}}'
        #award_url_2 = '[https://caching.graphql.imdb.com/?operationName=AdvancedTitleSearch&variables={"awardConstraint"%3A{"allEventNominations"%3A[{"eventId"%3A"ev0000292"}]}%2C"certificateConstraint"%3A{"anyRegionCertificateRatings"%3A[{"rating"%3A"R"%2C"region"%3A"US"}]%2C"excludeRegionCertificateRatings"%3A[]}%2C"creditedCompanyConstraint"%3A{"anyCompanyIds"%3A["co0023400"]%2C"excludeCompanyIds"%3A[]}%2C"first"%3A50%2C"genreConstraint"%3A{"allGenreIds"%3A["Crime"%2C"Thriller"]%2C"excludeGenreIds"%3A["Talk-Show"%2C"Reality-TV"%2C"News"%2C"Game-Show"%2C"Documentary"%2C"Short"]}%2C"locale"%3A"en-US"%2C"originCountryConstraint"%3A{"anyPrimaryCountries"%3A["US"]}%2C"rankedTitleListConstraint"%3A{"allRankedTitleLists"%3A[{"rankRange"%3A{"max"%3A5000%2C"min"%3A1}%2C"rankedTitleListType"%3A"TITLE_METER"}%2C{"rankRange"%3A{"max"%3A1000}%2C"rankedTitleListType"%3A"TOP_RATED_MOVIES"}]%2C"excludeRankedTitleLists"%3A[]}%2C"releaseDateConstraint"%3A{"releaseDateRange"%3A{"end"%3A"2024-12-31"%2C"start"%3A"1980-01-01"}}%2C"runtimeConstraint"%3A{"runtimeRangeMinutes"%3A{"max"%3A180%2C"min"%3A1}}%2C"sortBy"%3A"USER_RATING"%2C"sortOrder"%3A"DESC"%2C"titleCreditsConstraint"%3A{"allCredits"%3A[{"nameId"%3A"nm0000233"}%2C{"nameId"%3A"nm0000168"}]}%2C"titleTypeConstraint"%3A{"anyTitleTypeIds"%3A["movie"]%2C"excludeTitleTypeIds"%3A[]}%2C"userRatingsConstraint"%3A{"aggregateRatingRange"%3A{"max"%3A9.9%2C"min"%3A5}}}&extensions={"persistedQuery"%3A{"sha256Hash"%3A"60a7b8470b01671336ffa535b21a0a6cdaf50267fa2ab55b3e3772578a8c1f00"%2C"version"%3A1}}](https://caching.graphql.imdb.com/?operationName=AdvancedTitleSearch&variables=%7B%22awardConstraint%22%3A%7B%22allEventNominations%22%3A%5B%7B%22eventId%22%3A%22ev0000292%22%7D%5D%7D%2C%22certificateConstraint%22%3A%7B%22anyRegionCertificateRatings%22%3A%5B%7B%22rating%22%3A%22R%22%2C%22region%22%3A%22US%22%7D%5D%2C%22excludeRegionCertificateRatings%22%3A%5B%5D%7D%2C%22creditedCompanyConstraint%22%3A%7B%22anyCompanyIds%22%3A%5B%22co0023400%22%5D%2C%22excludeCompanyIds%22%3A%5B%5D%7D%2C%22first%22%3A50%2C%22genreConstraint%22%3A%7B%22allGenreIds%22%3A%5B%22Crime%22%2C%22Thriller%22%5D%2C%22excludeGenreIds%22%3A%5B%22Talk-Show%22%2C%22Reality-TV%22%2C%22News%22%2C%22Game-Show%22%2C%22Documentary%22%2C%22Short%22%5D%7D%2C%22locale%22%3A%22en-US%22%2C%22originCountryConstraint%22%3A%7B%22anyPrimaryCountries%22%3A%5B%22US%22%5D%7D%2C%22rankedTitleListConstraint%22%3A%7B%22allRankedTitleLists%22%3A%5B%7B%22rankRange%22%3A%7B%22max%22%3A5000%2C%22min%22%3A1%7D%2C%22rankedTitleListType%22%3A%22TITLE_METER%22%7D%2C%7B%22rankRange%22%3A%7B%22max%22%3A1000%7D%2C%22rankedTitleListType%22%3A%22TOP_RATED_MOVIES%22%7D%5D%2C%22excludeRankedTitleLists%22%3A%5B%5D%7D%2C%22releaseDateConstraint%22%3A%7B%22releaseDateRange%22%3A%7B%22end%22%3A%222024-12-31%22%2C%22start%22%3A%221980-01-01%22%7D%7D%2C%22runtimeConstraint%22%3A%7B%22runtimeRangeMinutes%22%3A%7B%22max%22%3A180%2C%22min%22%3A1%7D%7D%2C%22sortBy%22%3A%22USER_RATING%22%2C%22sortOrder%22%3A%22DESC%22%2C%22titleCreditsConstraint%22%3A%7B%22allCredits%22%3A%5B%7B%22nameId%22%3A%22nm0000233%22%7D%2C%7B%22nameId%22%3A%22nm0000168%22%7D%5D%7D%2C%22titleTypeConstraint%22%3A%7B%22anyTitleTypeIds%22%3A%5B%22movie%22%5D%2C%22excludeTitleTypeIds%22%3A%5B%5D%7D%2C%22userRatingsConstraint%22%3A%7B%22aggregateRatingRange%22%3A%7B%22max%22%3A9.9%2C%22min%22%3A5%7D%7D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22sha256Hash%22%3A%2260a7b8470b01671336ffa535b21a0a6cdaf50267fa2ab55b3e3772578a8c1f00%22%2C%22version%22%3A1%7D%7D)'
        #rating_count_url = 'https://caching.graphql.imdb.com/?operationName=AdvancedTitleSearch&variables={"awardConstraint"%3A{"allEventNominations"%3A[{"eventId"%3A"ev0000292"}]}%2C"certificateConstraint"%3A{"anyRegionCertificateRatings"%3A[{"rating"%3A"R"%2C"region"%3A"US"}]%2C"excludeRegionCertificateRatings"%3A[]}%2C"creditedCompanyConstraint"%3A{"anyCompanyIds"%3A["co0023400"]%2C"excludeCompanyIds"%3A[]}%2C"first"%3A50%2C"genreConstraint"%3A{"allGenreIds"%3A["Crime"%2C"Thriller"]%2C"excludeGenreIds"%3A["Talk-Show"%2C"Reality-TV"%2C"News"%2C"Game-Show"%2C"Documentary"%2C"Short"]}%2C"locale"%3A"en-US"%2C"originCountryConstraint"%3A{"anyPrimaryCountries"%3A["US"]}%2C"rankedTitleListConstraint"%3A{"allRankedTitleLists"%3A[{"rankRange"%3A{"max"%3A5000%2C"min"%3A1}%2C"rankedTitleListType"%3A"TITLE_METER"}]%2C"excludeRankedTitleLists"%3A[]}%2C"releaseDateConstraint"%3A{"releaseDateRange"%3A{"end"%3A"2024-12-31"%2C"start"%3A"1980-01-01"}}%2C"runtimeConstraint"%3A{"runtimeRangeMinutes"%3A{"max"%3A180%2C"min"%3A1}}%2C"sortBy"%3A"USER_RATING"%2C"sortOrder"%3A"DESC"%2C"titleCreditsConstraint"%3A{"allCredits"%3A[{"nameId"%3A"nm0000233"}%2C{"nameId"%3A"nm0000168"}]}%2C"titleTypeConstraint"%3A{"anyTitleTypeIds"%3A["movie"]%2C"excludeTitleTypeIds"%3A[]}%2C"userRatingsConstraint"%3A{"aggregateRatingRange"%3A{"max"%3A9.9%2C"min"%3A5}%2C"ratingsCountRange"%3A{"max"%3A3000000%2C"min"%3A100000}}}&extensions={"persistedQuery"%3A{"sha256Hash"%3A"60a7b8470b01671336ffa535b21a0a6cdaf50267fa2ab55b3e3772578a8c1f00"%2C"version"%3A1}}'

        #super_url = url_test(rating_count_url)
        #return {'data': super_url}

        #return {'url': search_url}
        #return {'data1': new_query}

        if len(movie_list) > search_data['selection_limit']:
            selected_movies = random_sample(movie_list, search_data['selection_limit'])
        else:
            selected_movies = movie_list

        return {'data': selected_movies, 'url': search_url}
    except Exception as err:
        return {'err': str((err))}

def testee(fff):
    
    return {"data": str(fff)}

if __name__ == "__main__":
    utils = json.loads(sys.argv[2])
    search_data = utils['search_utils']

    data = scrape_data_main(sys.argv[1])
    print(json.dumps(data))

