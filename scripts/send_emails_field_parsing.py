### This script send emails messages
### with specific fields for parsing in the HTMl body

# %% 
import pandas as pd
import os, sys
import html
from bs4 import BeautifulSoup
from glob import glob
from OAuth2_email import send_email
# from latest_file import find_most_recent_file


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

### Read the HTML content from an external file
with open("..\emails\email_field_parsing.html", "r", encoding="utf-8") as file:
    msgHtml = file.read()

### Convert HTML to plain text
soup = BeautifulSoup(msgHtml, "html.parser")
msgPlain = soup.get_text(separator="\n")

### Extract the subject from the meta tag
subject_tag = soup.find("meta", {"name": "email-subject"})
subject = subject_tag["content"] if subject_tag else "No Subject"

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
        subject=subject,
        msgHtml=msgHtml.format(reviewer_name=reviewer_name, list_of_abstracts=list_of_abstracts),
        msgPlain=msgPlain.format(reviewer_name=reviewer_name, list_of_abstracts=list_of_abstracts)
        )

# %%