import pandas as pd
import os, sys
import html
from OAuth2_email_test import send_email

### Provide filename of the PARSED WordPress export here
filename = "cybo-webinars-2024-registration-2024-04-15_14 06 53_parsed.csv"

### Provide surname of speaker here
speaker = "Riva"

### Paste the Zoom webinar invite here
# # could be opened from a txt file
# with open("D:\cybo_emails\zoom_riva.txt", "rb") as file: 
#     zoom_invite = file.read()

# # replacement strings because we need to fix the EoL...
# WINDOWS_LINE_ENDING = b'\r\n'
# UNIX_LINE_ENDING = b'\n'
# HTML_LINE_ENDING = b'<br/'
# print(zoom_invite.replace(WINDOWS_LINE_ENDING, HTML_LINE_ENDING))

# or hardcoded with multiline string
zoom_invite = r"""Luca Pegoraro is inviting you to a scheduled Zoom meeting.

Topic: CYBO Webinar - Federico Riva
Time: May 10, 2024 14:30 Zurich

Join Zoom Meeting
https://wsl.zoom.us/j/67839727760?pwd=V2lXRVZFeUVzL1ZmSjkvQzMvS0IrZz09

Meeting ID: 678 3972 7760
Passcode: 634406

---

One tap mobile
+31207947345,,67839727760# Netherlands
+31707006526,,67839727760# Netherlands

---

Dial by your location
• +31 20 794 7345 Netherlands
• +31 707 006 526 Netherlands
• +31 20 241 0288 Netherlands
• +31 20 794 0854 Netherlands
• +31 20 794 6519 Netherlands
• +31 20 794 6520 Netherlands

Meeting ID: 678 3972 7760

Find your local number: https://wsl.zoom.us/u/cbv15JBlX6

---

Join by SIP
• 67839727760@fr.zmeu.us

---

Join by H.323
• 213.19.144.110 (Amsterdam Netherlands)
• 213.244.140.110 (Germany)

Meeting ID: 678 3972 7760
Passcode: 634406"""

### Get emails for attendees of the specified webinar
data = pd.read_csv(filename, skipinitialspace=True) 
# print(data[data[speaker] == 1][['User Email', 'Do you need an attendance certificate?']])
# email_addresses = data[data[speaker] == 1 & data['Do you need an attendance certificate?'].str.contains('Yes')]['User Email']
email_addresses = ["luca.pegoraro@outlook.com"#, "maria.guerrina@edu.unige.it", "j.calevo@kew.org"] # for testing
]

### Send emails
for addressee in email_addresses: 
    # print(addressee, f"{pdf_path}\split\{certificate}")
    send_email(
        sender="conferenceyoungbotanists@gmail.com", 
        to=addressee,
        subject="CYBO test webinar invitation email 5", 
        msgHtml=f"Dear webinar participant,<br/>Please find below the Zoom meeting invite for the second CYBO webinar on May 10, 2024.<br/><br/>We hope to see you then!<br/>Kind regards,<br/>the CYBO steering committee.<br/><br/>{html.escape(zoom_invite)}<br/>", 
        msgPlain=f"Dear webinar participant,\nPlease find below the Zoom meeting invite for the second CYBO webinar on May 10, 2024.\n\nWe hope to see you then!\nKind regards,\nthe CYBO steering committee.\n\n{zoom_invite}\n"
        )