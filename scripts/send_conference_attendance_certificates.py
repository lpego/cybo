### This script uses the participants list
### to send the attendance certificates. 

# %% 
import pandas as pd
import os, sys
import html
from OAuth2_email import send_email

# %% Read in conference participants
participants = pd.read_csv("..\\website_exports\\presences_for_certificates.csv")

# %% Read in award winners
winners = pd.read_csv("..\\website_exports\\awards_for_certificates.csv")

# %% wrong certificates, to re-send
with open("..\\website_exports\\certificates_to_resend.txt", "r") as textfile: 
    resend = textfile.read().splitlines()
    # print(resend)
### Filter participants to re-send certificates
resend_participants = participants[participants['Name'].isin(resend)]

# # %% testing loop
# # for name, email, contribution, affiliation in participants[['Name', 'Email address', 'Contribution', 'Institution']].values:
# for name, email, contribution, affiliation in resend_participants[['Name', 'Email address', 'Contribution', 'Institution']].values:
#     print(name, "   ", email)
#     print("Contribution type: ", contribution)
#     print("Affiliation: ", affiliation)
#     filename = "Attendance_certificate_CYBO2025_" + name.replace(" ", "_") + ".pdf"
#     print("Does the file exist?     ", os.path.isfile("..\\certificates\\attendance_certificates\\" + filename))
#     print("=====================================")

# %% Send attendance certificate emails
# for name, email in participants[['Name', 'Email address',]].values:
for name, email in resend_participants[['Name', 'Email address',]].values:
    filename = "Attendance_certificate_CYBO2025_" + name.replace(" ", "_") + ".pdf"
    print("Sending email to: ", email)
    send_email(
        sender="conferenceyoungbotanists@gmail.com",
        ### normal addressees list
        to=email,
        # ### my emails for testing
        # to="luca.pegoraro@wsl.ch",
        subject="CYBO 2025 attendance certificate",
        msgHtml="""
        <p>Dear {name}, <br>
        &nbsp; apologies for the mistake, please find attached your corrected attendance certificate. <br><br>
                
        Kind regards, <br>
        CYBO organising committee.</p>
        """.format(name=name),
        msgPlain="""
        "Dear {name},\n
           apologies for the mistake, please find attached your corrected attendance certificate. \n\n
           
        Kind regards,\n
        CYBO organising committee.
        """.format(name=name),
        attachmentFile="..\\certificates\\attendance_certificates\\" + filename
        )

# # %% testing loop
# for name, email in winners[['Name', 'Email address',]].values:
#     print(name, email)
#     filename = "Award_certificate_CYBO2025_" + name.replace(" ", "_") + ".pdf"
#     print("Does the file exist?     ", os.path.isfile("..\\certificates\\award_certificates\\" + filename))
#     print("=====================================")

# # %% Send award certificate emails
# for name, email in winners[['Name', 'Email address',]].values:
#     filename = "Award_certificate_CYBO2025_" + name.replace(" ", "_") + ".pdf"
#     print("Sending email to: ", email)
#     send_email(
#         sender="conferenceyoungbotanists@gmail.com",
#         ### normal addressees list
#         to=email,
#         # ### my emails for testing
#         # to="luca.pegoraro@wsl.ch",
#         subject="CYBO 2025 award certificate",
#         msgHtml="""
#         <p>Dear {name}, <br>
#         &nbsp; we hope you enjoyed CYBO 2025! <br><br>
        
#         Please find attached your award certificate. <br><br>
        
#         We hope to see in future editions of CYBO! <br>
#         Kind regards, <br>
#         CYBO organising committee.</p>
#         """.format(name=name),
#         msgPlain="""
#         "Dear {name},\n
#            we hope you enjoyed CYBO 2025!\n\n
           
#         Please find attached your award certificate.\n\n
        
#         We hope to see in future editions of CYBO!\n
#         Kind regards,\n
#         CYBO organising committee.
#         """.format(name=name),
#         attachmentFile="..\\certificates\\award_certificates\\" + filename
#         )

# %%
