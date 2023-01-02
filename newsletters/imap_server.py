
import imaplib
from typing import Any, List
from utils import find_file_in_app
import json 


file_name = find_file_in_app('imap.json')
with open(file_name, 'r')  as f:
    creds = json.load(f)


def get_imap_server():
    # Connect to the server
    imap_server : Any = imaplib.IMAP4_SSL('imap.gmail.com')

    # Login to your account
    imap_server.login(creds['email_app'], creds['password_app'])

    # Select the INBOX mailbox
    imap_server.select('INBOX')

    return imap_server

# Iterate over the email IDs and delete each email
def delete_messages(imap_server, messages_to_delete):
    for message_id in messages_to_delete:
        imap_server.store(message_id, '+FLAGS', '\\Deleted')
