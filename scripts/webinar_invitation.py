### This script send webinar invitations, 
### uses external txt file for invite import

import pandas as pd
import os, sys
import html
from OAuth2_email import send_email

### Provide filename of the PARSED WordPress export here
filename = "cybo-webinars-2024-registration-2024-11-06_10_01_24_parsed.csv"

### Provide surname of speaker here
speaker = "Temunovic"

### Paste the Zoom webinar invite here; 
### could be opened from a txt file (more secure)...
with open("D:\cybo_emails\zoom_Temunovic.txt", "r") as file: 
    zoom_invite = file.read()

# ### ...or hardcoded with multiline string (might be useful for debugging)
# zoom_invite = """
# Someone is inviting you to a scheduled Zoom meeting.

# Topic: CYBO Webinar - Federico Riva
# Time: May 10, 2024 14:30 Zurich

# Join Zoom Meeting
# https://example.link.us/

# Meeting ID: 678 3972 7760
# Passcode: 634406

# [...]

# """

### Get emails for attendees of the specified webinar
data = pd.read_csv(filename, skipinitialspace=True)
# print(data[data[speaker] == 1][['User Email', 'Do you need an attendance certificate?']])
email_addresses = data[data[speaker] == 1]['User Email']
# email_addresses = ["luca.pegoraro@outlook.com"]

### Send emails
for addressee in email_addresses:
    print("Sending email to: ", addressee)
    send_email(
        sender="conferenceyoungbotanists@gmail.com",
        to=addressee,
        subject="CYBO webinar: Martina Temunovic - in 1 hour",
        msgHtml="""
        Dear webinar participant,<br/>
        The next CYBO webinar will start at 11:00am CET<br/>
        Find below the Zoom link.<br/>
        <br/>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br/>
        <br/>
        """ + html.escape(zoom_invite).replace('\n', '<br/>'),
        msgPlain="""
        Dear webinar participant,\n
        The next CYBO webinar will start at 11:00am CET.\n
        Find below the Zoom link.\n
        \n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n
        \n
        """ + html.unescape(zoom_invite),
        # attachmentFile="Webinar_10May_Riva-compressed.pdf" # check if attachment is needed
        )