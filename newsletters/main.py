import imaplib
import email
from email.message import Message
from tdlr import tldr_preprocessing
from parsers import main_parser
from typing import Tuple, List, Any
import json

with open('newsletters\\imap.json', 'r')  as f:
    creds = json.load(f)



imap_server: Any
# Connect to the server
imap_server = imaplib.IMAP4_SSL('imap.gmail.com')

# Login to your account
imap_server.login(creds['email_app'], creds['password_app'])

# Select the INBOX mailbox
imap_server.select('INBOX')

# Search for all messages in the INBOX mailbox
status, messages = imap_server.search(None, 'ALL')

# Get the message IDs of all messages found
message_ids = messages[0].split()

# Iterate through the messages
body_messages = []
body_message = ""
idx = 0
for message_id in message_ids:
    continue
    
    # Fetch the message data
    status, message_data = imap_server.fetch(message_id, '(RFC822)')
    message_data : List[Tuple[str,Any]]
    
    # Parse the message into a message object
    message : Message = email.message_from_bytes(message_data[0][1])

    # print(f'From: {message["From"]}')
    
    # Check if the sender is tldrnewsletter
    if 'tldrnewsletter' in message["From"]:
        body_messages += tldr_preprocessing(message)

# Extract articles content
# body_messages = [message for message in body_messages if message['publisher_onboarded'] ==True]
# with open('message.json','w') as f:
#     json.dump(body_messages,f)

# with open('responses.json','r') as f:
#     data = json.load(f)



# archive .ph is not onboarded
# After that, pass to chatgpt output and database storage
# create Django interface


with open('responses.json','r') as f:
    data = json.load(f)

# data = [d for d in data if d["publisher_onboarded"] ==True]
for d in data:
    domain_url = d['domain_url']
    body = d['body']
    url = d['url']
    print(main_parser(body, url, domain_url))
        

        
# Iterate over the email IDs and delete each email
# for message_id in message_ids:
#     server.store(message_id, '+FLAGS', '\\Deleted')

# Disconnect from the server
# imap_server.close()
# imap_server.logout()

# py .\newsletters\utils.py