# cybo_emails
Sending automated personalised emails using OAuth2 Gmail API

Following these tutorials: 
 - https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python 
 - https://realpython.com/python-send-email/#sending-multiple-personalized-emails 

 ## Trials & Tribulations
 SMTP is deprecated, need to use OAuth2. 

 **Update 1:** Successfully sent an "Hello World" using `OAuth2_email_test.py` pulled from [here](https://stackoverflow.com/a/40942045/7722773). Need to send attachments with it now. 

**Update 2:** successfully set up attachment sending, with help from further elaborations on the SO thread [here](https://stackoverflow.com/a/43379469/7722773) and [here](https://stackoverflow.com/a/49620786/7722773). The PDF attachments are blanks (i.e. empty) when opened! TESTED: only PDFs, images work fine...

**Update 3:** updated script `OAuth2_email_test.py` to correctly evaluate pdf MIMEtypes, thanks to [this](https://stackoverflow.com/a/11921241/7722773) now they send & open correctly. 

Base functionality running, next steps: 
 1. Implement parsing of names from Wordpress website users registration export. 
 2. Loop over names / emails to create personalised emails
    - Import `OAuth_email_test.py` as a module? 
 3. Figure out solution for personalised PDFs, possible routes: 
    - Use Overleaf as before (see [here](https://www.overleaf.com/project/660fa8e25e8920231dabd66e)) and figure out splitting PD in Python, leveraging known users order. 
    - Compile personalised certificates in LaTeX locally (but don't really want to deal with installation, so probably a Docker instead)

### Trying to make LaTeX compile in a Docker container for easy certificate generation
Inspiration from: 
 - https://medium.com/@kombustor/vs-code-docker-latex-setup-f84128c6f790 
 - https://medium.com/@timju/latex-setup-with-vs-code-and-docker-612f998e1f23 
 - https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop 

Current idea is to use the TeX workshop extension in VS code and go with their recommended Docker container. 