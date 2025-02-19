<a href="[https://conferenceyoungbotanists.com/](https://conferenceyoungbotanists.com/)"><img src="https://conferenceyoungbotanists.com/wp-content/uploads/2024/01/LogoCYBO_black-1110x530.png" align="center" width="480" ></a>

# CYBO website utilities
This repo contains all the scripts and utils to manage, automate and run the [CYBO](https://conferenceyoungbotanists.com/) website. 

Get a snapshot of private files like website exports, email lists, etc here (password protected): [CYBO private files archive](https://www.dropbox.com/scl/fi/tmzlut6dv853st162elc4/cybo_archive_2025-02-19_16-57-43.zip?rlkey=1emz6oxqitxcr0f9ljkno4n7w&st=9fishzlw&dl=0). 

## What's what
The main directories are: 
 - `certificates` - contains the produced files for certificates generation
 - `graphics` - assets for certificate generation and emails
 - `scripts` - contains all the python al LaTeX scripts, as well secrets (i.e. OAuth token)
 - `webinars` - contains the Zoom invites for the webinars
 - `website_exports`- is where most data is stored: WordPress website's users; manually curated lists of various kinds; website form exports; also exported HTML tables for pasting into the website, etc...

There is also a `.devcontainer` directory with details for Docker container deployment for this repo.

The section [Scripts](#scripts) is auto-generated based on short descriptions at the top of `.py` files. 

### Index
 - [Scripts](#scripts)
   - [Utilities](#utils)
   - [Parse users info](#parse-users-info)
   - [Generate LaTeX certificates](#generate-certificates)
 - [What to do for...](#what-to-do-for)
 - [Known bugs](#known-bugs)
 - [Dev notes](#dev-notes)

<!-- ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ### --> 
# Scripts

- `scripts/OAuth_token_refresh.py`: This script is useful to renew the OAuth2 token when expired
- `scripts/send_conference_attendance_certificates.py`: This script uses the participants list to send the attendance certificates.
- `scripts/parse_abstracts.py`: This script parses the abstracts form export, cleans rogue newlines, and writes out a reduced csv for further processing
- `scripts/make_latex_calls.py`: This scripts generates the LaTeX \confpin calls based on name patterns and file names
- `scripts/HTML_tables_posters.py`: This script reads in abstracts and sessions data and creates a HTML table with coloured sessions etc no need to read final sessions, since none were changed
- `scripts/parse_wp_users.py`: This script parses webinar registrations and grabs users's emails that have registered to a particular webinar.
- `scripts/send_acceptance_emails.py`: This script parses the reviewed abstract scores and sends acceptance emails to authors.
- `scripts/certificates_prep.py`: This script produces the LaTeX certificates for the webinar attendees
- `scripts/OAuth2_email.py`: These are the main functions to handle parsing of various arguments for email message composition and sending the message via the Gmail API
- `scripts/webinar_invitation.py`: This script send webinar invitations, uses external txt file for invite import
- `scripts/split_attendance_certificates.py`: This script splits the single PDF file into individual, personalised PDFs for each participant
- `scripts/HTML_table_talks.py`: This script reads in abstracts and sessions data and creates a HTML table with coloured sessions etc no need to read final sessions, since none were changed
- `scripts/update_readme.py`: Helper script to automatically grab the first couple lines of each script with the description of what it does, and update the README accordingly.
- `scripts/certificates_send.py`: This script send personalised emails with locally generated LaTeX certificates
- `scripts/create_qr_codes.py`: This scripts generates QR codes based on abstract URLs for name badges
- `scripts/send_reviewers_emails.py`: This script parses the compiled reviewer spreadsheet and sends emails to reviewers with their assigned abstracts.
- `scripts/parse_presences_for_certificates.py`: This script uses a manually curated list of attendees to the conference and merges it with abstract and evaluation data as well as curated institutions names to create the base data for certificate generation.
- `scripts/send_emails.py`: This script grabs email list from parse_users_emails.py and sends messages
- `scripts/merge_abstracts_evaluations.py`: This script merges the abstracts and reviewers' evaluations
- `scripts/zip_private_files.py`: This script puts all the files with sensitive information in a zip archive
- `scripts/parse_users_emails.py`: This script uses various exports to collect all user emails useful for sending newsletters, etc.
- `scripts/latest_file.py`: This is a small utility script to grab the most recent file version when filenames include datetime
## Utils
General-purpose utilities used in other scripts.  

 - `scripts/latest_file.py` a RegEx that grabs the most recent file given a list, using `glob` for instance; supports several `datetime` formats. 

 - `scripts/OAuth2_email.py` sends emails to a specified email address (implemented as `main` function), with attachment. ~~Supports also CC~~. 🐛 BUG: "cc" field is still broken...

<!-- ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ### -->
## Parse users info
`scripts/parse_*` and `scripts/merge_*` scripts handle the export files from WordPress plugin [User Registration](https://wordpress.org/plugins/user-registration/) and [Everest Forms](https://everestforms.net/) exports and convert them to a more usable format. 

<!-- ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ### -->
## Generate LaTeX certificates
Uses both `.py` and `.tex` scripts to generate LaTeX certificates based on website exports etc. 

 - `scripts/certificates_prep.py` loops over list of names pulled from registration from export and splits PDFs based on that. 
 - `scripts/create_qr_codes.py` creates QR codes for the abstract links to put on the nametags. 
 - `scripts/make_latex_calls.py` makes the \confpin calls to put in `nametags*.tex`. 
 - `scripts/split_attendance_certificates.py` split the multi-page PDF into individual, appropriately-named PDFs. 

⚠ compiling `.tex` files with pdflatex is usually fine, except when using the `fontspec` package, in that case use LuaLaTeX instead. 

 - `scripts/webinar_certificates.tex` takes a `.txt` file as input, with each row corresponding to a name, and generates certificates based on those. 
 - `scripts/nametags_*.tex` uses the `\confpin` generated by `make_latex_calls.py` to make conference badges with name, affiliation and QR code (for participants with contributions). 
 - `scripts/attendance_certificates.tex` and `scripts/award_certificates_landscape.tex` produce the attendance and award certificates for the conference, respectively, importing data from a dedicated `.csv` file generated by `parse_presences_for_certificates.py`. 


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
# Known bugs 🐛
If the the `.csv` export contains empty values for certain variables (e.g. "What webinars are you interested in?"), it will throw an error; could fix it with a `try` construct but seems unnecessary at this point... 

In dev container `LaTeX-custom-devcontainer`, on Windows the SSH agent doesn't communicate correctly with Docker, so authentication doesn't currently work (e.g. github). 

<!-- ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ### -->
# Changelog

[SECURITY UPDATE FEB 2025]: sanitised all scripts, no sensitive personal info appears anywhere in public files. 

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