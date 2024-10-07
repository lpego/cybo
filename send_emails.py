import pandas as pd
import os, sys
import html
from OAuth2_email_test import send_email

### Provide filename of the PARSED WordPress export here
filename = "cybo-webinars-2024-registration-2024-10-07_19_00_28_parsed.csv"

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
        subject="CYBO 2025 updates",
        msgHtml="""
        <p>Dear Young Botanists,<br>
        &nbsp;we have some exciting updates to share with you!<br><br>
        The CYBO 2025 conference will return to <strong>Genova</strong> (IT) on <strong>Febraury 5-7</strong>! Mark your calendar and check the <a href="https://conferenceyoungbotanists.com/2024/10/cybo-conference-2025-5-7-feb-genova">website</a> for more information in the very near future.<br><br>
        We also have changed our website address, now simply: <a rel="nofollow" target="_blank" href="https://conferenceyoungbotanists.com/">https://conferenceyoungbotanists.com/</a> (before it was <a href="https://conferenceyoungbotanists.000webhostapp.com/">this</a>).<br>
        Your username and password have been migrated, so you should be able to login as usual; you might have to manually find your credentials in your password manager though, as the domain has changed and therefore it probably won&apos;t auto-fill on the new website!<br><br>
        Finally, we are back with the fall webinar series, kicking off <strong>Oct 9th, 2:30-3:30 CET</strong> with <em>Laura M. Suz</em> (Royal Botanic Gardens, Kew): <em>&quot;Mycorrhizas and ecosystem function&quot;</em>. Head over to the registration page <a href="https://conferenceyoungbotanists.com/webinars-2024">here</a>.<br><br>
        Looking forward to see many of you online and soon in person!<br>
        CYBO organising committee.</p>
        """,
        msgPlain="""
        Dear Young Botanists, \n 
        we have some exciting updates to share with you! \n\n
        The CYBO 2025 conference will return to Genova (IT) on Febraury 5-7! Mark your calendar and check the website for more information in the very near future. \n\n
        We also have changed our website address, now simply https://conferenceyoungbotanists.com/ (before it was https://conferenceyoungbotanists.000webhostapp.com/). \n
        Your username and password have been migrated, so you should be able to login as usual; you might have to manually find your credentials in your password manager, as the website domain has changed and therefore it probably won't auto-fill them! \n\n
        Finally, we are back with the fall webinar series, kicking off  Oct 9th, 2:30-3:30 CET woth Laura M. Suz (Royal Botanic Gardens, Kew): Mycorrhizas and ecosystem function. Head over to the registration page here: https://conferenceyoungbotanists.com/webinars-2024 \n\n
        Looking forward to see many of you online and soon in person! \n
        CYBO organising committee. \n
        """,
        # attachmentFile="Webinar_10May_Riva-compressed.pdf" # check if attachment is needed
        )