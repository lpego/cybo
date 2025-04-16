### Script to parse HTML file and
### send emails with its contents

import pandas as pd
import os, sys
import html
from bs4 import BeautifulSoup
from OAuth2_email import send_email

### Read in conference participants
participants = pd.read_csv("..\\website_exports\\presences_for_certificates.csv")

### Read the HTML content from an external file
with open("..\\emails\\abstract_correction_photos.html", "r", encoding="utf-8") as file:
    msgHtml = file.read()

### Convert HTML to plain text
soup = BeautifulSoup(msgHtml, "html.parser")
msgPlain = soup.get_text(separator="\n")

### Extract the subject from the meta tag
subject_tag = soup.find("meta", {"name": "email-subject"})
subject = subject_tag["content"] if subject_tag else "No Subject"

### Send emails
for addressee in participants["Email address"]:
    print("Sending email to: ", addressee)
    send_email(
        sender="conferenceyoungbotanists@gmail.com",
        to=addressee,
        # ### my emails for testing
        # to="luca.pegoraro@outlook.com",
        # cc="luca.pegoraro@wsl.ch", 
        subject=subject,
        msgHtml=msgHtml,
        msgPlain=msgPlain,
    )