import httplib2
import os
import oauth2client
from oauth2client import client, tools, file
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
import argparse
import sys

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'scripts\client_secret.json'
APPLICATION_NAME = 'Gmail API Python Send Email'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-email-send.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def SendMessage(sender, to, cc, subject, msgHtml, msgPlain, attachmentFile=None):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    if attachmentFile:
        message1 = createMessageWithAttachment(sender, to, cc, subject, msgHtml, msgPlain, attachmentFile)
    else: 
        message1 = CreateMessageHtml(sender, to, cc, subject, msgHtml, msgPlain)      
    result = SendMessageInternal(service, "me", message1)
    return result


def SendMessageInternal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return "Error"
    return "OK"

def CreateMessageHtml(sender, to, cc, subject, msgHtml, msgPlain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    if cc:  # Include CC in headers only if provided
        msg['Cc'] = cc
    msg.attach(MIMEText(msgPlain, 'plain'))
    msg.attach(MIMEText(msgHtml, 'html'))
    # Combine 'To' and 'Cc' for the final recipient list
    all_recipients = [to] + ([cc] if cc else [])
    return {'raw': base64.urlsafe_b64encode(msg.as_string().encode()).decode(), 'to': all_recipients}


def createMessageWithAttachment(sender, to, cc, subject, msgHtml, msgPlain, attachmentFile):
    message = MIMEMultipart('mixed')
    message['to'] = to
    if cc:
        message['Cc'] = cc
    message['from'] = sender
    message['subject'] = subject

    messageA = MIMEMultipart('alternative')
    messageR = MIMEMultipart('related')

    messageR.attach(MIMEText(msgHtml, 'html'))
    messageA.attach(MIMEText(msgPlain, 'plain'))
    messageA.attach(messageR)

    message.attach(messageA)

    content_type, encoding = mimetypes.guess_type(attachmentFile)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    
    main_type, sub_type = content_type.split('/', 1)
    with open(attachmentFile, 'rb') as fp:
        if main_type == 'text':
            msg = MIMEText(fp.read(), _subtype=sub_type)
        elif main_type == 'image':
            msg = MIMEImage(fp.read(), _subtype=sub_type)
        elif main_type == 'audio':
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
        elif main_type == 'application':
            msg = MIMEApplication(fp.read(), _subtype=sub_type)
        else:
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
    
    filename = os.path.basename(attachmentFile)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    # Combine 'To' and 'Cc' for the final recipient list
    all_recipients = [to] + ([cc] if cc else [])
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode(), 'to': all_recipients}


# ### Hardcoded arguments    
# def send_email():
#     """Send email with attachment"""
#     to = "luca.pegoraro@outlook.com"
#     sender = "conferenceyoungbotanists@gmail.com"
#     subject = "CYBO emails - testing PDF attachments"
#     msgHtml = "Hi<br/>Html Email"
#     msgPlain = "Hi\nPlain Email"
#     ### Send message without attachment: 
#     # SendMessage(sender, to, subject, msgHtml, msgPlain)
#     ### Send message with attachment: 
#     SendMessage(sender, to, subject, msgHtml, msgPlain, 'D:\cybo\webinars_cybo2024_v4.1_compressed.pdf')

# if __name__ == '__main__':
#     send_email()

### Argument parsing
def send_email(sender, to, cc, subject, msgHtml, msgPlain, attachmentFile=None):
    """Send email with optional CC and attachment."""
    SendMessage(sender, to, cc, subject, msgHtml, msgPlain, attachmentFile)


if __name__ == "__main__":
   
    parser = argparse.ArgumentParser(description="Send email with attachments")
    parser.add_argument('--sender', type=str, required=True, help="Reply to field")
    parser.add_argument('--to', type=str, required=True, help="Address to send email to")
    parser.add_argument('--cc', type=str, required=False, help="Address to copy in")
    parser.add_argument('--subject', type=str, required=True, help="Subject text of the email")
    parser.add_argument('--msgHtml', type=str, required=True, help="HTML-formatted text body of the email")
    parser.add_argument('--msgPlain', type=str, required=False, help="Plain-text body of the email (for legacy clients)")
    parser.add_argument('--attachmentFile', type=str, required=False, help="Path to the attachment file")
    parser.add_argument('--verbose', "-v", action="store_true", help="Print function arguments")
    args = parser.parse_args()
    
    if args.verbose:
        print(f"args: {args}")

    sys.exit(send_email(args.sender, args.to, args.cc, args.subject, args.msgHtml, args.msgPlain, args.attachmentFile))

### CLI string to test: 
### python OAuth2_email_test.py --to "luca.pegoraro@outlook.com" --sender "conferenceyoungbotanists@gmail.com" --subject "CLI_test_email" --msgHtml "Hi<br/>Html Email" --msgPlain "Hi\nPlain Email" --attachmentFile D:\cybo_emails\webinars_cybo2024_v4.1_compressed.pdf --verbose