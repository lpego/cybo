import pandas as pd
import os, sys
import html
from OAuth2_email_test import send_email

# ### Provide filename of the PARSED WordPress export here
# filename = "cybo-webinars-2024-registration-2024-11-11_16_57_14_parsed.csv"

# ### Get emails for attendees (ALL of them)
# data = pd.read_csv(filename, skipinitialspace=True)
# # print(data[data[speaker] == 1][['User Email', 'Do you need an attendance certificate?']])
# email_addresses = data['User Email']
# email_addresses = ["luca.pegoraro@outlook.com"]
# # print(email_addresses)

# ### get email list 
with open("..\website_exports\email_list.txt") as f:
     email_addresses = [line.rstrip('\n') for line in f]
# print(type(email_addresses))
# print(email_addresses)

### Send emails
for addressee in email_addresses:
    print("Sending email to: ", addressee)
    send_email(
        sender="conferenceyoungbotanists@gmail.com",
        to=addressee,
        subject="CYBO registration deadline extended!",
        msgHtml="""
        <p>Dear Young Botanists, <br>
        &nbsp;if you missed the chance to submit a contribution to CYBO 2025, we have now extended the abstract submission deadline for talks and posters to <strong>Monday, December 23<sup>rd</sup>, 23:59 (CET)</strong>! Head over to the <a rel="nofollow" target="_blank" href="https://conferenceyoungbotanists.com/cybo-2025/cybo-2025-registration">registration page here</a> to submit your contribution. <br><br>
        We look forward to welcoming you in Genova! <br>
        Kind regards, <br>
        CYBO organising committee.</p>
        """,
        msgPlain="""
        Dear Young Botanists, \n
        if you missed the chance to submit a contribution to CYBO 2025, we have now extended the abstract submission deadaline for talks and posters to  Monday, December 23rd, 23:59 (CET)! Head over to https://conferenceyoungbotanists.com/cybo-2025/cybo-2025-registration to submit your contribution. \n\n
        We look forward to welcoming you in Genova! \n
        Kind regards, \n
        CYBO organising committee.
        """,
        # attachmentFile="Webinar_10May_Riva-compressed.pdf" # check if attachment is needed
        )