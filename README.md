# CYBO website utilities
This repo contains all the scripts and utils to manage, automate and run the [CYBO](https://conferenceyoungbotanists.com/) website. 

🛑 Need to recode all filepaths after repo re-organistaion... [not sure if I did that already for all scripts...]

## What's what
The main directories are: 
 - `certificates` - contains the produced files for certificates generation
 - `graphics` - assets for certificate generation and emails
 - `scripts` - contains all the python al LaTeX scripts
 - `webinars` - contains the Zoom invites for the webinars
 - `website_exports`- is where WordPress website's users info is stored

There is also a `.devcontainer` directory with details for Docker container deployment for this repo.

### Index
 - [Utilities](#utils)
 - [Parse users info](#parse-users-info)
 - [Send bulk emails](#send-bulk-emails)
 - [Generate certificates](#generate-certificates)
 - [What to do for...](#what-to-do-for)
 - [Known bugs](#known-bugs)
 - [Dev notes](#dev-notes)

<!-- ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ### -->
# Utils
General-purpose utilities used in other scripts here.  

 - `scripts/latest_file.py` a RegEx that grabs the most recent file given a list, using `glob` for instance; supports several `datetime` formats. 

 - `scripts/OAuth2_email_test.py` sends emails to a specified email address (implemented as `main` function), with attachment. Supports also CC. 

<!-- ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ### -->
# Parse users info
Handle the export files from WordPress plugin [User Registration](https://wordpress.org/plugins/user-registration/) and convert in a more usable format. 

 - `scripts/parse_wp_users` pulls out the list of user emails for each webinar from the export of WordPress's plugin User Registration. 
 
 - `scripts/merge_abstracts_evaluations.py` merges files from WordPress plugins [User Registration](https://wordpress.org/plugins/user-registration/) and [Everest Forms](https://everestforms.net/) exports, with assigned reviewers and handlers from Google Sheet export. 

<!-- ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ### -->
# Send bulk emails
Sending automated bulk personalised emails using OAuth2 Gmail API: reminders, webinar invitations and sending certificates. 

 - `scripts/certificates_send.py` sends the generated pdf certificates to webinar attendees. 

 - `scripts/webinar_invitation.py` sends invites to webinar attendees (need to fix plain text hardcoded Zoom invite). 

<!-- ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ### -->
# Generate certificates
Generate personalised certificates using a containerised LaTeX application and users data. 

 - `scripts/certificates_prep.py` loops over list of names pulled from registration from export and splits PDFs based on that. 

<!-- ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ### -->
# What to do for...
 - *Get participant emails, webinar info from website export*: on [CYBO's Word Press website](https://conferenceyoungbotanists.com/) go to Admin panel > User Registration form > Settings > Export > Select registration form. Save in this repo, then run `parse_wp_users` changing variable `filename`. 
 - *Send Zoom invitation to webinar participants*: run `webinar_invitation.py` and change the following variables: `filename`, `speaker` , `zoom_invite` (can save Zoom invitation either in text file or hardcoded in script) as well as the arguments in the `send_email` function call. 
 - *Send a regular email to participants*: run `send_emails.py` and change the following variables: `filename`, as well as the arguments in the `send_email` function call. 
 - *Generate LaTeX certificates locally with Docker*: 
    - run `certificates_prep.py` to generate participants list; 
    - in VS Code, open repo folder in dev container (Ctrl+Shift+P -> "Dev container: Open Folder in Container..."); in `certificates_autofill.tex` , change the aname of the speaker (line 137), title of the talk (line 137), and filename with participants (line 165); with VS Code extension LaTeX workshop, compile with "Recipe: pdflatex"; this should output a multipage PDF with all the participants names named `certificates_autofill.pdf`. 
    - in `certificates_prep.py`, uncomment the last block (lines 32-47) and re-run the script to split multi-page pdf into single, appropriately named pdfs. 
 - *Send certificates to webinar participants*: run `certificates_send.py` and change variables as above (requires certificates already generated and split). 
 - *"Token expired" error*: run `OAuth2_email_test.py` and follow browser-based authentication to renew it. Use hardcoded arguments (commented out in the script) if `argparse` mode fails. 

<!-- ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ### -->
# Known bugs
If the the `.csv` export contains empty values for certain variables (e.g. "What webinars are you interested in?"), it will throw an error; could fix it with a `try` construct but seems unnecessary at this point... 

In dev container `LaTeX-custom-devcontainer`, on Windows the SSH agent doesn't communicate correctly with Docker, so authentication doesn't currently work (e.g. github). 

<!-- ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ### -->
# Dev notes
<details>
  <summary>Keeping these just for legacy purposes, potentially useful for debugging in the future...</summary>
  
   ## OAuth emails
   Following these tutorials: 
   - https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python 
   - https://realpython.com/python-send-email/#sending-multiple-personalized-emails 
   SMTP is deprecated, need to use OAuth2. 

   **Update 1:** Successfully sent an "Hello World" using `OAuth2_email_test.py` pulled from [here](https://stackoverflow.com/a/40942045/7722773). Need to send attachments with it now. 

   **Update 2:** successfully set up attachment sending, with help from further elaborations on the SO thread [here](https://stackoverflow.com/a/43379469/7722773) and [here](https://stackoverflow.com/a/49620786/7722773). The PDF attachments are blanks (i.e. empty) when opened! TESTED: only PDFs, images work fine...

   **Update 3:** updated script `OAuth2_email_test.py` to correctly evaluate pdf MIMEtypes, thanks to [this](https://stackoverflow.com/a/11921241/7722773) now they send & open correctly. 

   **Update 4:** recoding the __main__ method in `OAuth2_email_test.py` to accept arguments iteratively, see [here](https://stackoverflow.com/a/42747728/7722773). 

   **Update 5:** `OAuth2_email_test.py` can be run from CLI (via `argparse`) or imported as module.  

   **Update 6:** created `webinar_invitation.py` to loop over list of names for each webinar and send personalised emails with the correct PDF (based on workflow that uses Overleaf, no local LaTeX yet). 

   **Update 7:** adapted Docker coonatiner image for local LaTeX PDF generation, imported .tex from Overleaf (dependencies installed at Docker build). 

   Base functionality running, next steps: 
   1. ~~Implement parsing of names from Wordpress website users registration export.~~
   2. ~~Loop over names / emails to create personalised emails~~
      - ~~Import `OAuth_email_test.py` as a module? ~~
      - ~~Implement argparse for the main function~~
   3. ~~Figure out solution for personalised PDFs, possible routes:~~ 
      - ~~Use Overleaf as before (see [here](https://www.overleaf.com/project/660fa8e25e8920231dabd66e)) and figure out splitting PDF in Python, leveraging known users order (see [here](https://stackoverflow.com/questions/70817546/how-do-i-split-a-pdf-using-python-every-page-that-contains-a-set-of-specific-un))~~ 
      - ~~Compile personalised certificates in LaTeX locally (but don't really want to deal with installation, so probably a Docker instead) -- *seems too much work for what it's worth...*~~

   ## Trying to make LaTeX compile in a Docker container for easy certificate generation
   Inspiration from: 
   - https://medium.com/@kombustor/vs-code-docker-latex-setup-f84128c6f790 
   - https://medium.com/@timju/latex-setup-with-vs-code-and-docker-612f998e1f23 
   - https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop 

   Current idea is to use the TeX workshop extension in VS code and go with their recommended Docker container. 

   **Update**: getting container from [here](https://github.com/qdm12/latexdevcontainer)... After various adaptation it works, and settings, terminal history are persistent! 
  
</details>