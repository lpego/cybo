# cybo_emails
Sending automated personalised emails using OAuth2 Gmail API

Following these tutorials: 
 - https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python 
 - https://realpython.com/python-send-email/#sending-multiple-personalized-emails 

 ## Trials & Tribulations
 SMTP is deprecated, need to use OAuth2. 

 Update 1: Successfully sent an "Hello World" using `OAuth2_email_test.py` pulled from [here](https://stackoverflow.com/a/40942045/7722773). Need to send attachments with it now. 

Update 2: successfully set up attachment sending, with help from further elaborations on the SO thread [here](https://stackoverflow.com/a/43379469/7722773) and [here](https://stackoverflow.com/a/49620786/7722773). The PDF attachments are blanks (i.e. empty) when opened! TESTED: only PDFs, images work fine...