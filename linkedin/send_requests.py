import json
import requests
import time 
from typing import List, Dict



SLEEP_TIME = 3

def send_requests() -> List[Dict]:

    with open('cookies.json','r') as f:
        cookies = json.load(f)

    with open('headers.json','r') as f:
        headers= json.load(f)

    data_responses = []
    
    params = {}
    params['decorationId'] = 'com.linkedin.voyager.dash.deco.search.SearchClusterCollection-174'
    params['q'] = 'all'

    response = requests.get(    
        'https://www.linkedin.com/voyager/api/search/dash/clusters?&query=(flagshipSearchIntent:SEARCH_MY_ITEMS_SAVED_POSTS,queryParameters:(savedPostType:List(ALL)))&start=0',
        params=params,
        cookies=cookies,
        headers=headers,)

    data = response.json()
    data_responses.append(data)
    pagination_token = data['data']['metadata']['paginationToken']
    total = data['data']['paging']['total']

    start = 0

    while(total!=0):

        start=start+10
        params['paginationToken'] = pagination_token
        params['start']=start

        response = requests.get(
            'https://www.linkedin.com/voyager/api/search/dash/clusters?query=(flagshipSearchIntent:SEARCH_MY_ITEMS_SAVED_POSTS)',
            params=params,
            cookies=cookies,
            headers=headers,
                            )
        if response.status_code!=200:
            print(response)
            break
        data = response.json()
        data_responses.append(data)
        pagination_token = data['data']['metadata']['paginationToken']
        total = data['data']['paging']['total']
        time.sleep(SLEEP_TIME)

    with open('data_responses.json','w') as f:
        json.dump(data_responses,f)
    
    return data_responses