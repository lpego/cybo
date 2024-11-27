import pandas as pd
import os, sys
import html
from OAuth2_email_test import send_email

### Provide filename of the PARSED WordPress export here
filename = "cybo-webinars-2024-registration-2024-11-11_16_57_14_parsed.csv"

### Get emails for attendees (ALL of them)
data = pd.read_csv(filename, skipinitialspace=True)
# print(data[data[speaker] == 1][['User Email', 'Do you need an attendance certificate?']])
email_addresses = data['User Email']
# email_addresses = ["luca.pegoraro@outlook.com"]
# print(email_addresses)

### Send emails
for addressee in email_addresses:
    print("Sending email to: ", addressee)
    send_email(
        sender="conferenceyoungbotanists@gmail.com",
        to=addressee,
        subject="CYBO 2025 registration open!",
        msgHtml="""
        <p>Dear Young Botanists,<br>
        &nbsp;the registration for CYBO 2025 is open!<br><br>
        Head over to the <a rel="nofollow" target="_blank" href="https://conferenceyoungbotanists.com/cybo-2025/cybo-2025-registration">registration page</a> and follow the instructions to either submit a contribution (poster or talk) or for attendance only. <br>
        Deadline for abstract submission is <strong>December 6<sup>th</sup></strong>, don't miss out!<br><br>
        CYBO organising committee.</p>
        """,
        msgPlain="""
        Dear Young Botanists, \n
        the registration for CYBO 2025 is open! \n\n
        Head over to the registration page https://conferenceyoungbotanists.com/cybo-2025/cybo-2025-registration and follow the instructions to either submit a contribution (poster or talk) or for attendance only. \n
        Deadline for abstract submission is December 6th, don't miss out! \n\n
        CYBO organising committee. \n
        """,
        # attachmentFile="Webinar_10May_Riva-compressed.pdf" # check if attachment is needed
        )