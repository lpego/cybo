import pandas as pd
import os, sys
from OAuth2_email_test import send_email

send_email(
    sender="cybotest20@gmail.com", 
    to="luca.pegoraro@outlook.com",
    subject="no attachment?", 
    msgHtml="Hi<br/>Html Email", 
    msgPlain="Hi\nPlain Email", 
    attachmentFile='D:\cybo_emails\webinars_cybo2024_v4.1_compressed.pdf'
    )
