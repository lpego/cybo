### This script parses the compiled reviewer spreadsheet
### and sends emails to reviewers with their assigned abstracts. 

# %% 
import pandas as pd
import os, sys
import html
from OAuth2_email_test import send_email
from glob import glob

# from latest_file import find_most_recent_file

### Get the data from: 
### https://docs.google.com/spreadsheets/d/1BMadWzY4oZoWmt86lfRpSVISu-6Q0NlssU-PvO2IiCE/edit?gid=55512928#gid=55512928

# ### Provide file lists here here
# filelist = glob("..\website_exports\cybo-2025-registration,-with-contribution*_redux.csv")
# filename = find_most_recent_file(filelist) # grab most recent version
# print("Reading from file: ", filename)

filename = ("..\website_exports\Abstracts list for evaluation - data_redux_parsed_FINAL.csv")
print("Reading from file: ", filename)
data = pd.read_csv(filename)

# %% Grab abstract links for each reviewer
abstracts = {}
for reviewer, link, handler in zip(data["Reviewer"], data["URL"], data["Handler"]): 
    print(reviewer, link, handler)
    if reviewer not in abstracts.keys(): 
        abstracts[reviewer] = []
    abstracts[reviewer].append(link)
print(abstracts)

# %% associate reviewer and handler email
# Group by 'Reviewer_email' and collect unique 'Handler_email'
addresses = data.groupby('Reviewer_email')['Handler_email'] \
                  .apply(lambda x: list(set(x))) \
                  .to_dict()
### Fill in missing addresses, can't have NaN
addresses["jacopo.calevo@gmail.com"] = ["luca.pegoraro@wsl.ch"]
addresses["luca.pegoraro@wsl.ch"] = ["luca.pegoraro@wsl.ch"]
addresses["maria.guerrina@edu.unige.it"] = ["luca.pegoraro@wsl.ch"]
print(addresses)

# %% Send emails with personalised abstract list of links. 
for addressee, email in zip(abstracts.items(), addresses.items()):
    print("Name of reviewer: ", addressee[0])
    reviewer_name = str(addressee[0]).title()
    print("Links to abstracts: ", addressee[1])
    list_of_abstracts = "<br>".join(addressee[1])
    print("-" * 30)
    print("Email of reviewer: ", email[0])
    reviewer_email = email[0]
    print("Email of handler: ", email[1])
    handler_email = email[1]
    print("~" * 30)
    print("Sending email TO: ", reviewer_email, "; and CC:", handler_email)
    print("=" * 30)
    send_email(
        sender="conferenceyoungbotanists@gmail.com",
        to=reviewer_email,
        cc=handler_email[0],
        # ### my emails for testing
        # to="luca.pegoraro@outlook.com",
        # cc="luca.pegoraro@wsl.ch", 
        subject="CYBO conference abstract review",
        msgHtml="""
        <p>Dear {reviewer_name}, <br>
        &nbsp;we hope this email finds you well. We are sending you the abstracts of submissions to CYBO 2025 to review, which you will find at the links below.<br><br>
        Here's how it's going to work: to read an abstract, follow one of the links below; to submit your scores you can follow the link to the evaluation form below, copy the link (i.e. URL) of the abstract and submit your scores; then, go back to this email and repeat for the other abstracts.<br><br>
        <strong>List of abstracts to review: </strong><br> 
        {list_of_abstracts}<br><br>
        <strong>Evaluation form (password: "CYBO_review_2025"): </strong><br> 
        <a href="https://conferenceyoungbotanists.com/abstract-evaluation-form">https://conferenceyoungbotanists.com/abstract-evaluation-form</a><br><br>
        In your evaluation please consider that: participants were not able to add formatting to the text (e.g. italics for species names); the maximum length of abstracts was limited to 500 words, and titles to 250 characters.<br><br>
        For your evaluation, please consider the participant career stage, and for each aspect detailed in the form starting from the middle of the scale, and raise or lower score if better or worse than average. You can also add a comment, max 300 words. All reviews will remain anonymous.<br><br>
        Once you are done, kindly reply to all in this email confirming that you did.<br><br>
        Kind regards, <br>
        CYBO organising committee.</p>
        """.format(reviewer_name=reviewer_name, list_of_abstracts=list_of_abstracts),
        msgPlain="""
        Dear {reviewer_name},\n 
        we hope this email finds you well. We are sending you the abstracts of submissions to CYBO 2025 to review, which you will find at the links below.\n
        Here's how it's going to work: to read an abstract, follow on of the links below; to submit your scores you can follow the link to the evaluation form below, copy the link (i.e. URL) of the abstract and submit your scores; then, go back to this email and repeat for the other abstracts.\n\n
        **List of abstracts to review:**\n
        {list_of_abstracts}\n\n
        **Evaluation form (password: "CYBO_review_2025"):**\n
        https://conferenceyoungbotanists.com/abstract-evaluation-form \n\n
        In your evaluation please consider that: participants were not able to add formatting to the text (e.g. italics for species names); the maximum length of abstracts was limited to 500 words, and titles to 250 characters.\n
        For your evaluation, please evaluate each aspect detailed in the form starting from the middle of the scale, and raise or lower the score if better or worse than average.\n
        Once you are done, kindly reply to all in this email confirming that you did.\n\n
        Kind regards,\n 
        CYBO organising committee.
        """.format(reviewer_name=reviewer_name, list_of_abstracts=list_of_abstracts),
        )

# %%
