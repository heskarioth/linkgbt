import json
import requests
import time 
from .parsers import *
from .send_requests import send_requests
from typing import List, Dict

def extract_linkedin_posts() -> List[Dict]:
    # data_responses = send_requests()
    with open('data_responses.json','r') as f:
        data_responses = json.load(f)
    post_objects : list = []
    post_metrics : dict = {}

    for data in data_responses:
        for idx in range(1,len(data['included'])):
            try:
                post_content = get_post_content(data,idx) #
                thumbnail_url = get_thumbnail_url(data,idx) 
                author_tagline = get_author_tagline(data,idx) #
                author_name = get_author_name(data,idx) #
                post_link = get_post_link(data,idx) #
                post_id = get_post_id(data,idx) # 
                post_link_id = get_post_link_id(data,idx) #
                post_likes = get_post_total_likes(data, idx)
                post_comments = get_post_total_comments(data, idx)
                post_reactions  = get_post_likes_per_reaction_type(data, idx)
                author_url = get_author_url(data,idx)
                if all([post_content,post_id,post_link_id,post_link,author_tagline,author_name,author_url]):
                    post_object = {
                        'post_id':post_id,
                        'post_link_id':post_link_id,
                        'post_content':post_content,
                        'post_link':post_link,
                        'author_tagline':author_tagline,
                        'author_name':author_name,
                        'author_url':author_url,
                        'thumbnail_url':thumbnail_url,
                        'post_metrics' : None
                        }
                    post_objects.append(post_object)
                elif all([post_likes,post_comments,post_reactions]):
                    post_reactions : Tuple
                    post_metric = {
                        post_reactions[0]:{
                            'post_likes': post_likes,
                            'post_comments': post_comments,
                            'post_reactions': post_reactions[1]
                        }
                    }
                    post_metrics.update(post_metric)
   
            except Exception as e:
                print(e)

    # merge metrics with post obj
    for post in post_objects:
        post_id = post['post_id']
        post['post_metrics'] = post_metrics.get(post_id,None)

    with open('output_final.json','w') as f:
        json.dump(post_objects,f)
    
    return post_objects