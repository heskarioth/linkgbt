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
from chatgpt_wrapper import ChatGPT
from typing import List
import html


from utils import find_file_in_app

file_name = find_file_in_app('imap.json')
with open(file_name, 'r')  as f:
    creds = json.load(f)

imap_server = get_imap_server(creds)


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

data_responses = parse_body_responses(data_responses)

# global_init()
print('Loading to database..')
print(svc.bulk_insert(contents=data_responses,collection=NewsletterArticle,document_type = NewsletterArticle))

with open('responses2.json','w') as f:
    json.dump(data_responses,f)


# linkedin_prompt_0 = "Hi can you help me? I've been working on a long post, but I want to rephrase it and make it suitable to share in my professional network in LinkedIn. It should be shorter than the original blog as well as more engaging. Can you help with that?"

# linkedin_prompt_1 = """
#      Thanks. This is the blog I wanted to make suitable for LinkedIn audiance:\n\n'REPLACE_TEXT_HERE'\n
#      Prompt instructions:
#      - Be ORIGINAL. You have to enrich the paragraphs with relevant details to make the text more engaging. You can use your internal training set and add relevant text to mine
#      - The post should be no more than 200-250 words, use subheadings and bullet points to break up the text.
#      - Craft a compelling headline for the post.
#      - Feel free to add emojis.
#      - Include a call to action in in the post to encourage my readers to take a specific action by asking thought provoking questions and engage with me. 
#      - Include hashtags to increase its visibility and help it reach a wider audience.
#      - It should be ready to go. Do not include your text or comments. Just the output.
# """
    
# linkedin_prompt_2 = """I like it. Do you think there's another way to make it more succint and more relavant to my audiance of entrepreneurs and software engineers?"""

# botgpt = ChatGPT()

# documents : List[NewsletterArticle] = svc.get_all_documents(NewsletterArticle)

# documents = [document for document in documents if document.has_chatgpt_content==False]

# n_responses = [0,450, 650]
# prompts = [linkedin_prompt_0, linkedin_prompt_1,linkedin_prompt_2]
# print('Fetching GPT responses..')
# for document in documents:
#     botgpt.new_conversation()
#     for idx,TEXT_MAN_LEN in enumerate(n_responses):
#         # get full text
#         full_text : str = html.unescape(str(document.article_original_body))
        
#         # select subsample of original text
#         full_text_reduced, _ = post_size_controller(full_text,TEXT_MAX_LEN = TEXT_MAN_LEN)
        
#         # prompt instruction
#         text_input = prompts[idx].replace('REPLACE_TEXT_HERE',full_text_reduced)

#         # send request to chat GPT
#         chatgpt_response = botgpt.ask(text_input)
#         if idx!=0:
#             document.chatgpt_post_content_attemps.append(chatgpt_response)
    
#     print(f'Created summary for : {document.id}')
#     # change status to GPT content flag
#     document.has_chatgpt_content=True
#     # save
#     document.save()
    


# we need to have an interface to check for content
# This interface should:
#   allow to select if content is ChatGPT material
#   approve post of new contents
#   schedule approved stuff

        
# Iterate over the email IDs and delete each email
# for message_id in message_ids:
#     server.store(message_id, '+FLAGS', '\\Deleted')

# Disconnect from the server
# imap_server.close()
# imap_server.logout()

# py .\newsletters\utils.py