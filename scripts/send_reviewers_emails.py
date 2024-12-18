### This script parses the compiled reviewer spreadsheet
### and sends emails to reviewers with their assigned abstracts. 

# %% 
import pandas as pd
import os, sys
import html
from OAuth2_email_test import send_email
from glob import glob

from latest_file import find_most_recent_file

### Provide file lists here here
filelist = glob("..\website_exports\cybo-2025-registration,-with-contribution*_redux.csv")
filename = find_most_recent_file(filelist) # grab most recent version
print("Reading from file: ", filename)

data = pd.read_csv(filename)

# %% Grab abstract links for each reviewer
abstracts = {}
for reviewer, link, handler in zip(data["Reviewer"], data["URL"], data["Handler"]): 
    # print(reviewer, link)
    if reviewer not in abstracts.keys(): 
        abstracts[reviewer] = []
    abstracts[reviewer].append(link)
# print(abstracts)

# %% Send emails with personalised abstract list of links. 
for addressee in abstracts.keys():
    ### define transient variables for HTML rendering
    list_of_abstracts = "<br>".join(abstracts[addressee])
    reviewer_name = str(addressee).capitalize()
    print("Sending email to: ", addressee)
    send_email(
        sender="conferenceyoungbotanists@gmail.com",
        # to=addressee,
        to="luca.pegoraro@outlook.com",
        cc="luca.pegoraro@wsl.ch", 
        subject="CYBO conference abstract review",
        msgHtml="""
        <p>Dear {reviewer_name}, <br>
        &nbsp;we hope this email finds you well. We are sending you the abstracts of submissions to CYBO 2025 to review, which you will find at the links below.<br><br>
        Here's how it's going to work: to read the an abstract, follow the links below; to submit your scores you can follow the link to the evaluation form below, and submit it; go back to this email, and repeat for the other abstracts.<br><br>
        <strong>List of abstracts to review: </strong><br> 
        {list_of_abstracts}<br><br>
        <strong>Evaluation form (password: "CYBO_review_2025"): </strong><br> 
        <a href="https://conferenceyoungbotanists.com/abstract-evaluation-form">https://conferenceyoungbotanists.com/abstract-evaluation-form</a><br><br>
        In your evaluation please consider that: participants were not able to add formatting to the text (e.g. italics for species names); the maximum length of abstracts was limited to 500 words, and titles to 250 characters.<br><br>
        For your evaluation, please consider the participant career stage, and for each aspect detailed in the form starting from the middle of the scale, and raise or lower score if better or worse than average. You can also add a comment, max 300 words. All reviews will remain anonymous.<br><br>
        Once you are done, kindly reply to this email confirming that you did.<br><br>
        Kind regards, <br>
        CYBO organising committee.</p>
        """.format(reviewer_name=reviewer_name, list_of_abstracts=list_of_abstracts),
        msgPlain="""
        Dear {reviewer_name},\n 
        we hope this email finds you well. We are sending you the abstracts of submissions to CYBO 2025 to review, which you will find at the links below.\n
        Here's how it's going to work: to read an abstract, follow the links below; to submit your scores you can follow the link to the evaluation form below, and submit it; go back to this email, and repeat for the other abstracts.\n\n
        **List of abstracts to review:**\n
        {list_of_abstracts}\n\n
        **Evaluation form (password: "CYBO_review_2025"):**\n
        https://conferenceyoungbotanists.com/abstract-evaluation-form \n\n
        In your evaluation please consider that: participants were not able to add formatting to the text (e.g. italics for species names); the maximum length of abstracts was limited to 500 words, and titles to 250 characters.\n
        For your evaluation, please evaluate each aspect detailed in the form starting from the middle of the scale, and raise or lower the score if better or worse than average.\n
        Once you are done, kindly reply to this email confirming that you did.\n\n
        Kind regards,\n 
        CYBO organising committee.
        """.format(reviewer_name=reviewer_name, list_of_abstracts=list_of_abstracts),
        )

# %%
