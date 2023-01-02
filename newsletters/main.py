import email
from email.message import Message
from .tdlr import tldr_preprocessing
from .parsers import parse_body_responses, post_size_controller
from typing import Tuple, List, Any, Dict
import json
from .imap_server import get_imap_server
from .utils import run_search_content
from database.models import NewsletterArticle
import controller.services as svc
# from chatgpt_wrapper import ChatGPT
from chat import update_documents_with_chatgpt_posts
from typing import List
import html

imap_server = get_imap_server()

body_messages = [] # keep body responses

messages_to_delete = [] # keep id of emails to delete

# Search for all messages in the INBOX mailbox
status, messages = imap_server.search(None, 'ALL')

# Get the message IDs of all messages found
message_ids = messages[0].split()

# Iterate through the messages
print('Extracting news articles from newsletters...')
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


print('Search for articles contents...')
# only get data from onboarded publishers
body_messages = [message for message in body_messages if message['publisher_onboarded'] ==True]

# we actually want to store the entire body response. we only want chatgpt to make summary later. We ask for two summaries: body 450 wordcount, body 600 wordcount.
# scrape body messages
data_responses : List[Dict] = run_search_content(body_messages)

# parse data responses
# we should do the parsing only on onboarded providers
print('Parsing the responses...')
data_responses = [response for response in data_responses if response['publisher_onboarded'] ==True]

with open('responses2.json','w') as f:
    json.dump(data_responses,f)


data_responses = parse_body_responses(data_responses)

# global_init()
print('Loading to database..')
print(svc.bulk_insert(contents=data_responses,collection=NewsletterArticle,document_type = NewsletterArticle))


update_documents_with_chatgpt_posts()


# we need to have an interface to check for content
# This interface should:
#   allow to select if content is ChatGPT material
#   approve post of new contents
#   schedule approved stuff




# Disconnect from the server
# imap_server.close()
# imap_server.logout()

# py .\newsletters\utils.py