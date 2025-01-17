### This script parses the reviewed abstract scores
### and sends acceptance emails to authors. 

# %% 
import pandas as pd
import os, sys
import html
from OAuth2_emails import send_email
from glob import glob

from latest_file import find_most_recent_file

### Get the data from: 
### https://docs.google.com/spreadsheets/d/1BMadWzY4oZoWmt86lfRpSVISu-6Q0NlssU-PvO2IiCE/edit?gid=1671145313#gid=1671145313

# %% grab data
# ### Provide file lists here
# filelist = glob("..\website_exports\merged_abstracts_evaluations_*.csv")
# filename = find_most_recent_file(filelist) # grab most recent version
# print("Reading from file: ", filename)

### grab final version
filename = "..\website_exports\Abstracts list for evaluation - merged_abstracts_evaluations_2025-01-16_12-16-04_FINAL.csv"
print("Reading from file: ", filename)

data = pd.read_csv(filename).drop(['Unnamed: 0'],axis=1)
# Replace NaN values in the 'General comments' column with the string 'none'
data['General comments'] = data['General comments'].fillna('none')

# # %% testing loop
# for name, surname, email, contrib_type, session, abs_aims, abs_methods, abs_discussion, comment in data[['First Name', 'Last Name', 'Email address', 
#                                                 'Final contribution', 'Final session', 
#                                                 'The project has well defined aims and tasks.', 'The approach/analysis is sound and well explained.', 'The research will likely stimualte discussions at the conference.', 'General comments',]].values:
#     participant = f"{str(name).title()} {str(surname).title()}"
#     print(participant, email)
#     print(contrib_type, session)
#     print(abs_aims, abs_methods, abs_discussion)
#     print(comment)
#     print("=====================================")

# %% send emails
for name, surname, email, contrib_type, session, abs_aims, abs_methods, abs_discussion, comment in data[['First Name', 'Last Name', 'Email address', 
                                                'Final contribution', 'Final session', 
                                                'The project has well defined aims and tasks.', 'The approach/analysis is sound and well explained.', 'The research will likely stimualte discussions at the conference.', 'General comments',]].values:
    participant = f"{str(name).title()} {str(surname).title()}"
    print("Sending email to: ", email)
    send_email(
        sender="conferenceyoungbotanists@gmail.com",
        ### normal addressees list
        to=email,
        # ### my emails for testing
        # to="luca.pegoraro@wsl.ch",
        # cc="luca.pegoraro@outlook.com", 
        subject="CYBO contribution acceptance and important info",
        msgHtml="""
        <p>Dear {participant}, <br>
        &nbsp; we are writing to inform you that your contribution has been accepted as a <strong>{contrib_type}</strong>, in session <strong>"{session}"</strong> at CYBO 2025!<br><br>
        
        At least one member of the scientific committee reviewed your abstract, and provided a score from 1 to 10 for three categories, and had the option to leave a comment. 
        You can find the evaluation scores and comment, if available, below. 
        <ul>
            <li><i>The project has well defined aims and tasks.</i> &nbsp; {abs_aims} / 10; </li>
            <li><i>The approach/analysis is sound and well explained.</i> &nbsp; {abs_methods} / 10; </li>
            <li><i>The research will likely stimulate discussions at the conference.</i> &nbsp; {abs_discussion} / 10.</li>
            <li><i>Reviewer comment:</i> &nbsp; {comment}</li>
        </ul>
        
        For talks, the assigned time slot will be 12 minutes, with 3 minutes for questions, and they must be prepared as single .ppt, .pptx or .pdf file. <br>
        For posters, the format must be A0 portrait (i.e. vertical): 841 mm wide × 1189 mm high; it is not possible to accommodate horizontal posters. <br>
        Further details will be published shortly on the <a href="https://conferenceyoungbotanists.com/cybo-2025">conference page</a>. <br><br>
        
        The draft program for the conference is available on the website, and you can find it <a href="https://conferenceyoungbotanists.com/cybo-2025/cybo-2025-programme">here</a>. <br> 
        A detailed program with individual time slots and locations for talks and posters will be available shortly. <br><br>
        
        If we have not yet received your payment for the conference, you will receive a follow-up email; if you have already paid, no further action is required. <br><br>
        
        <strong>IMPORTANT:</strong> to accommodate the many contributions, the venue for the conference has changed! It will now take place at the DAD, located in the historical centre of Genova: <br>
        Department of Architecture and Design (DAD), Stradone di Sant'Agostino 37, 16123 Genova (Italy); <a href="https://maps.app.goo.gl/6ta5jrAacKcgwD5t6">Google Maps</a>.<br>
        You can find more information on the <a href="https://conferenceyoungbotanists.com/cybo-2025/cybo-2025-venue-information">conference website</a>, along with a list of suggested hotels and B&Bs.<br><br>

        As a conference participant, you are cordially invited to the <strong>social dinner</strong>, taking place on <strong>February 6<sup>th</sup></strong>; find more information and reserve your space <a href="https://conferenceyoungbotanists.com/cybo-2025/cybo-social-dinner">here</a>. <br><br>
        
        We are looking forward to seeing you in Genova! <br>
        Kind regards, <br>
        CYBO organising committee.</p>
        """.format(participant=participant, email=email, 
                   contrib_type=contrib_type, session=session, 
                   abs_aims=abs_aims, abs_methods=abs_methods, abs_discussion=abs_discussion, comment=comment),
        msgPlain="""
        Dear {participant}, \n
        we are writing to inform you that your contribution has been accepted as a **{contrib_type}**, in session **"{session}"** at CYBO 2025!\n\n

        At least one member of the scientific committee reviewed your abstract, and provided a score from 1 to 10 for three categories, and had the option to leave a comment. \n
        You can find the evaluation scores and comment, if available, below. \n
        - *The project has well defined aims and tasks.* {abs_aims} / 10 \n
        - *The approach/analysis is sound and well explained.* {abs_methods} / 10 \n
        - *The research will likely stimulate discussions at the conference.* {abs_discussion} / 10 \n
        - *Reviewer comment:* {comment} \n\n

        For talks, the assigned time slot will be 12 minutes, with 3 minutes for questions, and they must be prepared as single .ppt, .pptx or .pdf file. \n
        For posters, the format must be A0 portrait (i.e. vertical): 841 mm wide × 1189 mm high; it is not possible to accommodate horizontal posters. \n
        Further details will be published shortly on the [conference page](https://conferenceyoungbotanists.com/cybo-2025). \n\n

        The draft program for the conference is available on the website, and you can find it [here](https://conferenceyoungbotanists.com/cybo-2025/cybo-2025-programme). \n
        A detailed program with individual time slots and locations for talks and posters will be available shortly. \n\n

        If we have not yet received your payment for the conference, you will receive a follow-up email; if you have already paid, no further action is required. \n\n

        **IMPORTANT:** to accommodate the many contributions, the venue for the conference has changed! It will now take place at the DAD, located in the historical centre of Genova: \n
        Department of Architecture and Design (DAD), Stradone di Sant'Agostino 37, 16123 Genova (Italy); [Google Maps](https://maps.app.goo.gl/6ta5jrAacKcgwD5t6). \n
        You can find more information on the [conference website](https://conferenceyoungbotanists.com/cybo-2025/cybo-2025-venue-information), along with a list of suggested hotels and B&Bs. \n\n

        As a conference participant, you are cordially invited to the **social dinner**, taking place on **February 6<sup>th</sup>**; find more information and reserve your space [here](https://conferenceyoungbotanists.com/cybo-2025/cybo-social-dinner). \n\n

        We are looking forward to seeing you in Genova! \n
        Kind regards, \n
        CYBO organising committee.
        """.format(participant=participant, email=email, 
                   contrib_type=contrib_type, session=session, 
                   abs_aims=abs_aims, abs_methods=abs_methods, abs_discussion=abs_discussion, comment=comment),
        )

# %%
