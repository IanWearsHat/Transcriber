import time
import keyboard
import imaplib
import email
from email.header import decode_header
import os

# Godaddy IMAP server: imap.secureserver.net
IMAP_SERVER = "outlook.office365.com"

"""
Username in first line
Password in second line
"""
def get_credentials():
    with open('credentials.txt', 'r') as f:
        lines = f.readlines()
        return lines[0].strip(), lines[1].strip()


def login():
    usr, pwd = get_credentials()

    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(usr, pwd)

    return imap


def check_for_emails(imap):
    status, messages = imap.select("INBOX")

    messages = int(messages[0])
    print(status, messages)


def main():
    imap = login()
    check_for_emails(imap)

    # run = True
    # while run:
    #     if keyboard.is_pressed('p'):
    #         run = False
    #
    #     check_for_emails(imap)
    #
    #     time.sleep(0.02)


if __name__ == '__main__':
    main()
