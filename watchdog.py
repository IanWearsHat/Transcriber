import time
import keyboard
import os
import imaplib
import email
from email.header import decode_header
import pathlib

debug = False
PDFS_ONLY = False

IMAP_SERVER = "outlook.office365.com"
EMAIL_FOLDER = "INBOX"


"""
    Username in first line
    Password in second line
"""
def get_credentials():
    with open('credentials.txt', 'r') as f:
        lines = f.readlines()
        return lines[0].strip(), lines[1].strip()


class Watchdog:
    def __init__(self):
        self.imap = self.login()

    def login(self):
        usr, pwd = get_credentials()

        imap_obj = imaplib.IMAP4_SSL(IMAP_SERVER)
        imap_obj.login(usr, pwd)

        return imap_obj

    def check_for_attachments(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    # only download if the attachment is a pdf and it doesn't already exist

                    # really for in case we need all attachments
                    if PDFS_ONLY:
                        if ".pdf" in filename and not pathlib.Path(filename).is_file():
                            self.download_attachment(part, filename)
                    else:
                        if not pathlib.Path(filename).is_file():
                            self.download_attachment(part, filename)

    def download_attachment(self, part, filename):
        attachment_dir = os.path.join(os.path.abspath(__file__), '..', 'attachments')
        if not os.path.exists(attachment_dir):
            os.mkdir(attachment_dir)

        filepath = os.path.join(attachment_dir, filename)
        open(filepath, "wb").write(part.get_payload(decode=True))

    def fetch_all_emails(self, msg_num_list):
        for msg_num in msg_num_list:
            res, msg = self.imap.fetch(msg_num.decode(), "(RFC822)")  # fetch email by id
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])

                    if debug:
                        print('\n')
                        print(msg["Message-ID"])
                        print(msg["From"])
                        print(msg["Subject"])

                    self.check_for_attachments(msg)

    def check_for_emails(self, *, inbox_type):
        self.imap.select(EMAIL_FOLDER, readonly=True)  # readonly=True so that unread messages retain unread flag
        status, messages = self.imap.search(None, inbox_type)

        if status == "OK":

            if debug:
                print("All message IDs:\t", [num for num in messages[0].split()])

            self.fetch_all_emails(messages[0].split())

    def start(self):
        self.check_for_emails(inbox_type="(UNSEEN)")
        # self.check_for_emails(inbox_type="(INBOX)")


def main():
    Watchdog().start()

    # run = True
    # while run:
    #     if keyboard.is_pressed('p'):
    #         run = False
    #
    #     check_for_new_emails(imap)
    #
    #     time.sleep(0.02)

    # chance that the pdf downloaded is not what we're looking for
    # make file that notes down every pdf we've downloaded already
    # this is ensured by some id that uniquely identifies the cost
    # from the company


if __name__ == '__main__':
    main()
