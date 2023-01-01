
import imaplib
from typing import Any


def get_imap_server(creds):
    # Connect to the server
    imap_server : Any = imaplib.IMAP4_SSL('imap.gmail.com')

    # Login to your account
    imap_server.login(creds['email_app'], creds['password_app'])

    # Select the INBOX mailbox
    imap_server.select('INBOX')

    return imap_server
