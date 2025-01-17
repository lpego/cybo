import html
from OAuth2_email import SendMessage

### Hardcoded arguments    
def send_email():
    """Send email with attachment"""
    to = "luca.pegoraro@outlook.com"
    cc = "luca.pegoraro@wsl.ch"
    sender = "conferenceyoungbotanists@gmail.com"
    subject = "CYBO emails - testing PDF attachments"
    msgHtml = "Hi<br/>Html Email"
    msgPlain = "Hi\nPlain Email"
    ### Send message without attachment: 
    SendMessage(sender, to, subject, msgHtml, msgPlain)
    # ### Send message with attachment: 
    # SendMessage(sender, to, cc, subject, msgHtml, msgPlain, 'D:\cybo\webinars_cybo2024_v4.1_compressed.pdf')

if __name__ == '__main__':
    send_email()