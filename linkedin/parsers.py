
import re 
from typing import Tuple

def get_post_content(data,idx) -> str|None:
    if 'summary' in data['included'][idx].keys():
        text = data['included'][idx]['summary'].get('text',None)
        if text:
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            return '\n'.join(lines)

def get_thumbnail_url(data,idx) -> str|None:
    # there must be a better way to get all keys and just check they exist
    if 'entityEmbeddedObject' in data['included'][idx].keys():
        if 'image' in data['included'][idx]['entityEmbeddedObject'].keys():
            if 'vectorImage' in data['included'][idx]['entityEmbeddedObject']['image']['attributes'][0]['detailDataUnion'].keys():
                root_url = data['included'][idx]['entityEmbeddedObject']['image']['attributes'][0]['detailDataUnion']['vectorImage']['rootUrl']
                leaf_url = data['included'][idx]['entityEmbeddedObject']['image']['attributes'][0]['detailDataUnion']['vectorImage']['artifacts'][0]['fileIdentifyingUrlPathSegment']
                return root_url + leaf_url
    return None 


def get_author_name(data,idx):
    if 'title' in data['included'][idx].keys():
        return data['included'][idx]['title']['text']
    return None

def get_author_tagline(data,idx):
    if 'primarySubtitle' in data['included'][idx].keys():
        return data['included'][idx]['primarySubtitle']['text']
    return None

def get_post_link(data, idx):
    if 'overflowActions' in data['included'][idx].keys():
        post_link = data['included'][idx]['overflowActions'][2]['actionDetailsUnion']['shareViaLinkAction']['url'].split('?update')[0]
        post_link = 'https://www.linkedin.com/feed/update/'+data['included'][idx]['trackingUrn']
        return post_link
    return None

def get_post_id(data,idx):
    if 'trackingUrn' in data['included'][idx].keys():
        return data['included'][idx]['trackingUrn'].replace('urn:li:activity:','')
    return None



def get_post_link_id(data,idx) -> str|None:
    if re.findall(r"\d+", data['included'][idx]['entityUrn']):
        return str(re.findall(r"\d+", data['included'][idx]['entityUrn'])[0])


def get_post_likes_per_reaction_type(data, idx) -> Tuple|None:
    reactions = {}
    if 'reactionTypeCounts' not in data['included'][idx].keys():
        return None
    for row in data['included'][idx]['reactionTypeCounts']:
        count = row['count']
        reaction_type = row['reactionType']
        reactions[reaction_type]=count
    
    post_id = get_post_link_id(data,idx)
    return (post_id,reactions)


def get_post_total_likes(data,idx) -> int|None:
    return data['included'][idx].get('numLikes',None)

def get_post_total_comments(data,idx) -> int|None:
    return data['included'][idx].get('numComments',None)


def get_author_url(data,idx) -> str|None:
    if 'actorNavigationUrl' in data['included'][idx].keys():
        return data['included'][idx]['actorNavigationUrl']
    return None

