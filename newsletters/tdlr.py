
# from html import unescape
from bs4 import BeautifulSoup
import xmltodict
import urllib.parse as parser
from typing import List, Dict
import tld
import hashlib
import re 
from .ds import ArticleItem
from dataclasses import asdict

def tldr_preprocessing(message) -> List[Dict]:
    
    articles = []
    # Check if the message is an HTML message
    if message.is_multipart():
        
        for part in message.get_payload():
            
            # Find the first HTML part
            if part.get_content_type() == 'text/html':
                
                # Use BeautifulSoup to parse the HTML and extract the text
                soup = BeautifulSoup(part.get_payload(decode=True), 'html.parser')
#               
                # Convert the parsed HTML back into a string
                html_string = soup.prettify()
                json_object = xmltodict.parse(html_string)
                # json_object= json_object['div']['div']['div'][1]['div']['table']['tbody']['tr']['td']['table']['tbody']['tr']['td']['table']['tbody']['tr'][1]['td']['table']['tbody']['tr']['td']['table'][2:][:-2]
                json_object= json_object['html']['body']['table']['tbody']['tr']['td']['table']['tbody']['tr']['td']['table']['tbody']['tr'][1]['td']['table']['tbody']['tr']['td']['table'][2:][:-2]
                # adding generic publishers handled
                # temp removed: 'github.com', 'thedefiant.io',
                generic_publishers = ['bitcoinist.com', 'reuters.com', 'stevenbuccini.com', 'decrypt.co', 'cnbc.com', 'borretti.me', 'therecord.com', 'arstechnica.com', 'npr.org', 'medium.com', 'cnet.com', 'blockworks.co', 'dev.to', 'theguardian.com', 'electrek.co', 'freethink.com', 'digitaltrends.com', 'ieee.org', 'techcrunch.com', 'mirror.xyz', 'nypost.com', 'coindesk.com', 'macrumors.com', 'mit.edu', 'substack.com', 'techtimes.com', 'bitcoinmagazine.com', 'fortressofdoors.com', 'ethresear.ch', 'misfra.me', 'theverge.com', 'bitcoininsider.org', 'nbcnews.com', 'tbray.org', 'politico.com']
                
                # custom handled publishers
                custom_publishers = ['engadget','theweek','archive','businessinsider']
                
                list_publishers = generic_publishers + custom_publishers
                

                
                for idx in range(len(json_object)):
                    try:
                        title = json_object[idx]['tbody']['tr']['td']['div']['span']['a']['span']['strong']
                        title = re.sub(r'\( *\d+ *minute *read *\)', '', title)
                        preview = json_object[idx]['tbody']['tr']['td']['div']['span']['span']['#text']
                        url = json_object[idx]['tbody']['tr']['td']['div']['span']['a']['@href']    
                        url = parser.unquote(url).replace('https://tracking.tldrnewsletter.com/CL0/','').split('?utm_source=')[0]
                        domain_url = tld.get_fld(url, fail_silently=True)
                        publisher_onboarded = any([publisher for publisher in list_publishers if publisher in url])
                        articles.append(ArticleItem(
                            hashlib.md5(url.encode()).hexdigest(),
                            url,
                            title,
                            preview,
                            domain_url,
                            publisher_onboarded,
                            0,
                            "",
                            0
                            ))
                    except KeyError as key:
                        pass 
                break
        articles_dicts = [asdict(article) for article in articles]
        return articles_dicts
    else:
        # The message is not an HTML message, so just get the payload as a string
        return [{}]


