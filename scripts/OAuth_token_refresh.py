import html
from OAuth2_email import SendMessage

### Hardcoded arguments    
def send_email():
    """Send email with attachment"""
    to = "luca.pegoraro@outlook.com"
    # cc = "luca.pegoraro@wsl.ch"
    cc = None
    sender = "conferenceyoungbotanists@gmail.com"
    subject = "CYBO emails - testing email sending"
    msgHtml = "Hi<br/>Html Email"
    msgPlain = "Hi\nPlain Email"
    # ### Send message without attachment: 
    # SendMessage(sender, to, subject, msgHtml, msgPlain)
    ### Send message with attachment: 
    attachmentFile = 'D:\cybo\webinars_cybo2024_v4.1_compressed.pdf'
    SendMessage(sender, to, subject, msgHtml, msgPlain, cc, attachmentFile)

if __name__ == '__main__':
    send_email()