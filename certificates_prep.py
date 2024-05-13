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

with open(f"certificate_names_{speaker}.txt", "w") as file:
    for line in certificates_names: 
        file.write(f"{line}\n")
        
### Start devcontainer and generate multi-page PDF, copy it inside "certificates\{speaker}"

# ### Extract PDF pages, in order of participant
# pdf_path = f"D:\cybo_emails\certificates\{speaker}"
# inputpdf = PdfReader(open(f"{pdf_path}\certificates_autofill.pdf", "rb"))

# if not os.path.exists(f"{pdf_path}\split"):
#     os.makedirs(f"{pdf_path}\split")

# certificates_list = []
# for i in range(len(inputpdf.pages)):
#     output = PdfWriter()
#     output.add_page(inputpdf.pages[i])
#     name = certificates_names[i].replace(" ", "_")
#     # print(name)
#     certificates_list.append(f"Certificate_CYBO_webinar_10May2024_{name}.pdf")
#     with open(f"{pdf_path}\split\Certificate_CYBO_webinar_10May2024_{name}.pdf", "wb") as outputStream:
#         output.write(outputStream)