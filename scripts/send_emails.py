### This script grabs email list from
### parse_users_emails.py and sends messages

import pandas as pd
import os, sys
import html
from OAuth2_email import send_email

# ### Provide filename of the PARSED WordPress export here
# filename = "cybo-webinars-2024-registration-2024-11-11_16_57_14_parsed.csv"

# ### Get emails for attendees (ALL of them)
# data = pd.read_csv(filename, skipinitialspace=True)
# # print(data[data[speaker] == 1][['User Email', 'Do you need an attendance certificate?']])
# email_addresses = data['User Email']
# email_addresses = ["luca.pegoraro@outlook.com"]
# # print(email_addresses)

# ### get email list 
with open("website_exports\email_list.txt") as f:
     email_addresses = [line.rstrip('\n') for line in f]
# print(type(email_addresses))
# print(email_addresses)

### Send emails
for addressee in email_addresses:
    print("Sending email to: ", addressee)
    send_email(
        sender="conferenceyoungbotanists@gmail.com",
        to=addressee,
        subject="CYBO webinar, today 2pm: Franziska Willems",
        msgHtml="""
        <p>Dear Young Botanists, <br>
        &nbsp;please find below the link for the next CYBO webinar, <strong>today at 2pm</strong>, by Franziska Willems, Philipps University of Marburg (DE), entitled: “How and why is wildflower phenology changing over the last century?“<br>
        <a href="https://teams.microsoft.com/l/meetup-join/19%3ameeting_YzIzZTRmYmYtMTQ1YS00ZTZmLWFiNGUtODU0YzBhY2MxMGM1%40thread.v2/0?context=%7b%22Tid%22%3a%226cd36f83-1a02-442d-972f-2670cb5e9b1a%22%2c%22Oid%22%3a%22b17c2380-aac4-4307-aaa4-036f94f36f63%22%7d">Microsoft Teams meeting link</a>.<br><br>
        Kind regards, <br>
        CYBO organising committee.</p>
        """,
        msgPlain="""
        Dear Young Botanists, \n
        please find below the link for the next CYBO webinar, today at 2pm, by Franziska Willems, Philipps University of Marburg (DE), entitled: “How and why is wildflower phenology changing over the last century?“\n
        https://teams.microsoft.com/l/meetup-join/19%3ameeting_YzIzZTRmYmYtMTQ1YS00ZTZmLWFiNGUtODU0YzBhY2MxMGM1%40thread.v2/0?context=%7b%22Tid%22%3a%226cd36f83-1a02-442d-972f-2670cb5e9b1a%22%2c%22Oid%22%3a%22b17c2380-aac4-4307-aaa4-036f94f36f63%22%7d">Microsoft Teams meeting link</a>.\n\n
        Kind regards, \n
        CYBO organising committee.
        """,
        # attachmentFile="Webinar_10May_Riva-compressed.pdf" # check if attachment is needed
        )