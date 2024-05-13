import pandas as pd
import os, sys
from string import capwords
# import time
from pypdf import PdfWriter, PdfReader
from OAuth2_email_test import send_email

### Provide filename of the PARSED WordPress export here
filename = "cybo-webinars-2024-registration-2024-05-10_13 21 39_parsed.csv"

### Provide surname of speaker
speaker = "Riva"

### Get emails for attendees of the specified webinar
data = pd.read_csv(filename, skipinitialspace=True) 
email_addresses = data[data[speaker] == 1 & data['Do you need an attendance certificate?'].str.contains('Yes')]['User Email']
# email_addresses = ["luca.pegoraro@outlook.com", "maria.guerrina@edu.unige.it", "j.calevo@kew.org"] # for testing

### Make certificates names txt file for Overleaf
names = data[data[speaker] == 1 & data['Do you need an attendance certificate?'].str.contains('Yes')]['First Name']
surnames = data[data[speaker] == 1 & data['Do you need an attendance certificate?'].str.contains('Yes')]['Last Name']
certificates_names = [m.strip()+" "+n.strip() for m,n in zip(names,surnames)]
certificates_names = [capwords(x) for x in certificates_names]
# certificates_names = ["Luca Pegoraro", "Maria Guerrina", "Jacopo Calevo"] # for testing
        
### Extract PDF pages, in order of participant
pdf_path = f"D:\cybo_emails\certificates\{speaker}"
inputpdf = PdfReader(open(f"{pdf_path}\certificates_autofill.pdf", "rb"))

certificates_list = []
for i in range(len(inputpdf.pages)):
    output = PdfWriter()
    output.add_page(inputpdf.pages[i])
    name = certificates_names[i].replace(" ", "_")
    # print(name)
    certificates_list.append(f"Certificate_CYBO_webinar_{name}.pdf")

### Send emails
for name, addressee, certificate in zip(certificates_names, email_addresses, certificates_list): 
    print(name, addressee, f"{pdf_path}\split\{certificate}")
    # time.sleep(.5) # optional: give the server a little time before sending new one
    send_email(
        sender="conferenceyoungbotanists@gmail.com", 
        to=addressee,
        subject="CYBO webinar certificate - 10 May 2024", 
        msgHtml="""
        Dear webinar participant,<br/>
        Please find enclosed the participation certificate for the second CYBO webinar of May <sup>10</sup>, 2024.<br/><br/>
        We hope to welcome you again for the following webinars in September!<br/>
        Kind regards,<br/>
        CYBO steering committee.
        """, 
        msgPlain="""
        Dear webinar participant,\n
        Please find enclosed the participation certificate for the second CYBO webinar of May 10, 2024.\n\n
        We hope to welcome you again for the following webinars in September!\n
        Kind regards,\n
        CYBO steering committee.
        """, 
        attachmentFile=f"{pdf_path}\split\{certificate}"
        )