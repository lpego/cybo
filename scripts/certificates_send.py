### This script send personalised emails
### with locally generated LaTeX certificates

import pandas as pd
import os, sys
from string import capwords
# import time
from pypdf import PdfWriter, PdfReader
from OAuth2_email import send_email

### Provide filename of the PARSED WordPress export here
filename = "cybo-webinars-2024-registration-2024-11-11_16_57_14_parsed.csv"

### Provide surname of speaker
speaker = "Temunovic"

### Get emails for attendees of the specified webinar
data = pd.read_csv(filename, skipinitialspace=True) 
email_addresses = data[data[speaker] == 1 & data['Do you need an attendance certificate?'].str.contains('Yes')]['User Email']
# email_addresses = ["luca.pegoraro@outlook.com"] # for testing

### Make certificates names txt file for Overleaf
names = data[data[speaker] == 1 & data['Do you need an attendance certificate?'].str.contains('Yes')]['First Name']
surnames = data[data[speaker] == 1 & data['Do you need an attendance certificate?'].str.contains('Yes')]['Last Name']
certificates_names = [m.strip()+" "+n.strip() for m,n in zip(names,surnames)]
certificates_names = [capwords(x) for x in certificates_names]
# certificates_names = ["Luca Pegoraro"] # for testing
        
### Get PDF paths, in order of participant
pdf_path = f"D:\cybo_emails\certificates\{speaker}"

certificates_list = []
for name in certificates_names:
    # print(cert)
    certificates_list.append(f"Certificate_CYBO_webinar_06Nov2024_{name}.pdf".replace(" ", "_"))
# certificates_list = [f"Certificate_CYBO_webinar_09Oct2024_Luca_Pegoraro.pdf"] # for testing

### Send emails
for name, addressee, certificate in zip(certificates_names, email_addresses, certificates_list): 
    print(name, "-", addressee, "-", f"{pdf_path}\split\{certificate}")
    # time.sleep(.5) # optional: give the server a little time before sending new one
    send_email(
        sender="conferenceyoungbotanists@gmail.com", 
        to=addressee,
        subject="CYBO webinar certificate - 6 Nov 2024", 
        msgHtml="""
        Dear webinar participant,<br/>
        Please find enclosed the participation certificate for the fifth CYBO webinar on Nov 6<sup>th</sup>, 2024.<br/><br/>
        We hope to welcome you again for the next webinar!<br/><br/>
        Kind regards,<br/>
        CYBO steering committee.
        """, 
        msgPlain="""
        Dear webinar participant,\n
        Please find enclosed the participation certificate for the fifth CYBO webinar of Nov 6, 2024.\n\n
        We hope to welcome you again for the next webinar!\n\n
        Kind regards,\n
        CYBO steering committee.
        """, 
        attachmentFile=f"{pdf_path}\split\{certificate}"
        )