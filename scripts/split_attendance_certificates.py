### This script splits the single PDF file
### into indivdual, personalised PDFs for each participant

# %%
import pandas as pd
import os, sys
from string import capwords
# import time
from pypdf import PdfWriter, PdfReader
from OAuth2_email import send_email

# %% Read in file used for certificates generation
data = pd.read_csv('..\website_exports\presences_for_certificates.csv')
names = data["Name"].tolist() # grab list of names

# %% Prepare folders for splitting
pdf_path = f"..\\certificates"
if not os.path.exists(f"{pdf_path}\\attendance_certificates"):
    os.makedirs(f"{pdf_path}\\attendance_certificates")
    
inputpdf = PdfReader(open(f"{pdf_path}\\attendance_certificates.pdf", "rb"))

# %% Extract PDF pages, in order of participant
certificates_list = []
for i in range(len(inputpdf.pages)):
    output = PdfWriter()
    output.add_page(inputpdf.pages[i])
    name = names[i].replace(" ", "_")
    print(name)
    certificates_list.append(f"Attendance_certificate_CYBO2025_{name}.pdf")
    with open(f"{pdf_path}\\attendance_certificates\\Attendance_certificate_CYBO2025_{name}.pdf", "wb") as outputStream:
        output.write(outputStream)