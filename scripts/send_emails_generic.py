### Script to parse HTML file and
### send emails with its contents

import pandas as pd
import os, sys
import html
from bs4 import BeautifulSoup
from OAuth2_email import send_email

### get email list 
with open("..\website_exports\email_list.txt") as f:
     email_addresses = [line.rstrip('\n') for line in f]
# print(type(email_addresses))
# print(email_addresses)

### Read the HTML content from an external file
with open("..\emails\email_content.html", "r", encoding="utf-8") as file:
    msgHtml = file.read()

### Convert HTML to plain text
soup = BeautifulSoup(msgHtml, "html.parser")
msgPlain = soup.get_text(separator="\n")

### Extract the subject from the meta tag
subject_tag = soup.find("meta", {"name": "email-subject"})
subject = subject_tag["content"] if subject_tag else "No Subject"

### Send emails
for addressee in email_addresses:
    print("Sending email to: ", addressee)
    send_email(
        sender="conferenceyoungbotanists@gmail.com",
        # to=addressee,
        ### my emails for testing
        to="luca.pegoraro@outlook.com",
        cc="luca.pegoraro@wsl.ch", 
        subject=subject,
        msgHtml=msgHtml,
        msgPlain=msgPlain,
        # attachmentFile="Webinar_10May_Riva-compressed.pdf" # check if attachment is needed
    )