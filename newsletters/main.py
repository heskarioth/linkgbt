import email
from email.message import Message
from tdlr import tldr_preprocessing
from parsers import main_parser
from typing import Tuple, List, Any, Dict
import json
from imap_server import get_imap_server
from utils import run_search

with open('newsletters\\imap.json', 'r')  as f:
    creds = json.load(f)

imap_server = get_imap_server(creds)


body_messages = [] # keep body responses

messages_to_delete = [] # keep id of emails to delete

# Search for all messages in the INBOX mailbox
status, messages = imap_server.search(None, 'ALL')

# Get the message IDs of all messages found
message_ids = messages[0].split()

# Iterate through the messages
for message_id in message_ids:
    
    # Fetch the message data
    status, message_data = imap_server.fetch(message_id, '(RFC822)')
    message_data : List[Tuple[str,Any]]
    
    # Parse the message into a message object
    message : Message = email.message_from_bytes(message_data[0][1])

    # print(f'From: {message["From"]}')
    
    # Check if the sender is tldrnewsletter
    if 'tldrnewsletter' in message["From"]:
        body_messages += tldr_preprocessing(message)
        messages_to_delete.append(message_id)

# only get data from onboarded publishers
body_messages = [message for message in body_messages if message['publisher_onboarded'] ==True]


# we actually want to store the entire body response. we only want chatgpt to make summary later. We ask for two summaries: body 450 wordcount, body 600 wordcount.
# scrape body messages
data_responses : List[Dict] = run_search(body_messages)

# parse data responses
# we should do the parsing only on onboarded providers
data_responses = [response for response in data_responses if response['publisher_onboarded'] ==True]
for data in data_responses:
    parsed_result = main_parser(data['article_original_body'],data['article_url'],data['article_domain_url'])
    data['wordcount'] = parsed_result['word_count']
    data['article_original_body'] = parsed_result['full_text']
    

with open('responses2.json','w') as f:
    json.dump(data_responses,f)

# print(data_responses[0])

# with open('message.json','w') as f:
#     json.dump(body_messages,f)

# with open('responses.json','r') as f:
#     data = json.load(f)

# After that, pass to chatgpt output and database storage
# create Django interface

# with open('responses.json','r') as f:
#     data = json.load(f)

# # data = [d for d in data if d["publisher_onboarded"] ==True]
# for d in data:
#     domain_url = d['domain_url']
#     body = d['body']
#     url = d['url']
#     print(main_parser(body, url, domain_url))
        

        
# Iterate over the email IDs and delete each email
# for message_id in message_ids:
#     server.store(message_id, '+FLAGS', '\\Deleted')

# Disconnect from the server
# imap_server.close()
# imap_server.logout()

# py .\newsletters\utils.py