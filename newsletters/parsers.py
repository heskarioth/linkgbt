
from bs4 import BeautifulSoup
from requests import Response
import pandas as pd
from typing import Tuple
import re 



def archiveph_logic(soup : BeautifulSoup) -> dict:
    st = "background-position:initial;background-repeat:initial;-webkit-background-clip:border-box;color:rgb(0, 0, 0);font-family:Independent, serif;font-size:18px;font-stretch:100%;font-style:normal;font-variant-caps:normal;font-variant-east-asian:normal;font-variant-ligatures:normal;font-variant-numeric:normal;font-weight:400;background-attachment:scroll;background-clip:border-box;background-color:rgba(0, 0, 0, 0);background-image:none;background-origin:padding-box;background-size:auto;border-bottom-color:rgb(0, 0, 0);border-bottom-style:none;border-bottom-width:0px;border-image-outset:0;border-image-repeat:stretch;border-image-slice:100%;border-image-source:none;border-image-width:1;border-left-color:rgb(0, 0, 0);border-left-style:none;border-left-width:0px;border-right-color:rgb(0, 0, 0);border-right-style:none;border-right-width:0px;border-top-color:rgb(0, 0, 0);border-top-style:none;border-top-width:0px;box-sizing:border-box;display:block;line-height:1.55;margin-bottom:0px;margin-left:0px;margin-right:0px;margin-top:0px;outline-color:rgb(0, 0, 0);outline-style:none;outline-width:0px;padding-bottom:0px;padding-left:0px;padding-right:0px;padding-top:0px;vertical-align:baseline;width:100%;"
    full_text = []
    for div in soup.find_all('div',{'style':st}):
        txt = str(div.text)
        if txt not in full_text:
            full_text.append(txt)
    if len(full_text)==0:
        print('Archive ph broken')
        return {'full_text' : 0, 'word_count' : 0}
    full_text, word_count = post_size_controller(full_text)
    return {'full_text' : full_text, 'word_count' : word_count}



def businessinsider_logic(soup : BeautifulSoup) -> dict:
    full_text = ""
    for p in soup.find_all('p'):
        full_text=full_text+p.text
    full_text, word_count = post_size_controller(full_text)
    return {'full_text' : full_text, 'word_count' : word_count}





def theweek_logic(soup : BeautifulSoup) -> dict:
    full_text = []
    for div in soup.find_all({'div':'duet--article--article-body-component'}):
        for p in div.find_all('p')[:-1]:
            if p.text not in full_text:
                full_text.append(p.text)
        
    full_text, word_count = post_size_controller(full_text)
    return {'full_text' : full_text, 'word_count' : word_count}


# def generic_logic(soup : BeautifulSoup) -> dict:
#     full_text = []
#     for div in soup.find_all({'div':'duet--article--article-body-component'}):
#         for p in div.find_all('p')[:-1]:
#             if p.text not in full_text:
#                 full_text.append(p.text)
        
#     full_text, word_count = post_size_controller(full_text)
#     return {'full_text' : full_text, 'word_count' : word_count}

def generic_logic(soup : BeautifulSoup, url : str) -> dict:
    full_text = []
    for div in soup.find_all({'div':'duet--article--article-body-component'}):
        for p in div.find_all('p')[:-1]:
            if p.text not in full_text:
                full_text.append(p.text)
    if len(full_text)==0:
        raise ValueError(f'Error: No text parsed for {url}')
    full_text, word_count = post_size_controller(full_text)
    return {'full_text' : full_text, 'word_count' : word_count}
# not onboarded : threadreaderapp.com, bloomberg.com


def main_parser(text : str, url : str, domain: str) -> dict:
    soup = BeautifulSoup(text, 'html.parser')
    if domain=='businessinsider.com':
        data = businessinsider_logic(soup)
    elif domain=='theweek.com':
        pass
    elif domain=='archive.ph': 
        data = archiveph_logic(soup)
    elif domain in ['bitcoinist.com', 'reuters.com', 'stevenbuccini.com', 'decrypt.co', 'cnbc.com', 'borretti.me', 'therecord.com', 'arstechnica.com', 'npr.org', 'medium.com', 'cnet.com', 'blockworks.co', 'dev.to', 'theguardian.com', 'electrek.co', 'freethink.com', 'digitaltrends.com', 'github.com', 'thedefiant.io', 'ieee.org', 'techcrunch.com', 'mirror.xyz', 'nypost.com', 'coindesk.com', 'macrumors.com', 'uiverse.io', 'mit.edu', 'substack.com', 'techtimes.com', 'bitcoinmagazine.com', 'fortressofdoors.com', 'ethresear.ch', 'misfra.me', 'theverge.com', 'bitcoininsider.org', 'nbcnews.com', 'tbray.org', 'politico.com']:
        data = generic_logic(soup,url)
    else:
        data = {}
    return data


# Setting Max default size of text to be scraped.
def post_size_controller(full_text) -> Tuple:
    
    TEXT_MAX_LEN = 20
    
    # Split the string into sentences using a regular expression
    full_text = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', ''.join(full_text))
    data = pd.DataFrame([(k,f,len(f.split())) for k,f in enumerate(full_text)],columns=['idx','text','wordcount'])
    source_word_count = data['wordcount'].sum()
    TEXT_MAX_LEN = TEXT_MAX_LEN if source_word_count >=  TEXT_MAX_LEN  else source_word_count
    new_df = pd.DataFrame(columns=['idx','text','wordcount'])
    if data.shape[0]==0:
        # no data to return
        return (0,0)
    while True:
        sample : pd.DataFrame = data.sample().copy()
        wordcount  = sample['wordcount'].values[0]
        idx  = sample['idx'].values[0]
        if idx not in new_df.idx.to_list():
            new_df = pd.concat([new_df,sample])
        TEXT_MAX_LEN=TEXT_MAX_LEN-wordcount
        if TEXT_MAX_LEN<0:
            break
    new_df = new_df.drop_duplicates(subset=['text'])
    new_full_text = new_df.sort_values(by='idx')['text'].to_list()
    new_full_text = ''.join(new_full_text)
    new_word_count = new_df.wordcount.sum()
    return (new_full_text, new_word_count)

# I would like you to help me rephrease and improve this article of mine. It needs to be published on my linkedin network. 
# Target audiance: software engineers and AI researchers.
# Goal: increase my number of connections.
# Prompt instructions regarding the post:
#     - Be ORIGINAL. You have to enrich the paragraphs with relevant details to make the text more engaging.
#     - The post should be no more than 150-200 words, use subheadings and bullet points to break up the text.
#     - Craft a compelling headline for the post.
#     - Feel free to add emojis.
#     - Include a call to action in in the post to encourage my readers to take a specific action by asking thought provoking questions. 
#     - Include hashtags to increase its visibility and help it reach a wider audience.
#     - only output the text response. I do not wish to read your comments.
# ''
# Remember my prompts. You are NOT required to make a summary. 
# You are required to MAKE A LINKEDIN POST. 
# DO NOT EXCEED THE WORDCOUNT. 
# DO NOT FORGET CAUSAL INFERENCE.




# def cnet_logic(soup : BeautifulSoup) -> dict:
#     full_text = []
#     for div in soup.find_all({'div':'duet--article--article-body-component'}):
#         for p in div.find_all('p')[:-1]:
#             if p.text not in full_text:
#                 full_text.append(p.text)        
#     full_text, word_count = post_size_controller(full_text)
#     return {'full_text' : full_text, 'word_count' : word_count}

# def freethink_logic(soup : BeautifulSoup) -> dict:
#     full_text = []
#     for div in soup.find_all({'div':'duet--article--article-body-component'}):
#         for p in div.find_all('p')[:-1]:
#             if p.text not in full_text:
#                 full_text.append(p.text)
        
#     full_text, word_count = post_size_controller(full_text)
#     return {'full_text' : full_text, 'word_count' : word_count}

# def theverge_logic(soup : BeautifulSoup) -> dict:
#     full_text = []
#     for div in soup.find_all({'div':'duet--article--article-body-component'}):
#         for p in div.find_all('p')[:-1]:
#             if p.text not in full_text:
#                 full_text.append(p.text)
        
#     full_text, word_count = post_size_controller(full_text)
#     return {'full_text' : full_text, 'word_count' : word_count}


