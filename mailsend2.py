import os
from pathlib import Path
import smtplib
import email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import sys
from email.mime.text import MIMEText
import pymongo
import datetime
import time
recipients =[]
subject=""
body=""
data = []
def sendMailRonak(subjectt,subsubdept,message,data1):
    global COMMASPACE
    global recipients
    global subject
    global body
    global data
    data = data1;
    COMMASPACE = ', '
    if (type(subsubdept)=="lst"):
        
        recipients =subsubdept
    else:
        recipients =[subsubdept]
    reminder_mails=['tejas.choudhari15@outlook.com']
    reminder_numbers=[9930894939]
    subject = subjectt

    is_reminder=0
    sender = 'foodwastagemanger@gmail.com'
    body = message+str(datetime.datetime.now())
    main(sender,recipients,subject,body,is_reminder,reminder_mails,reminder_numbers)


def dbcreate():
    now = datetime.datetime.now()
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    if "EmailDB" not in myclient.list_database_names():
        emaildb = myclient["EmailDB"]
        email_sent = emaildb["emails_sent"]
        email_inbox = emaildb["emails_inbox"]
        email_sent.insert_one({'Date_Created':now.isoformat()})
        email_inbox.insert_one({'Date_Created':now.isoformat()})
        
    else:
        emaildb = myclient["EmailDB"]
        email_sent = emaildb["emails_sent"]
    return email_sent

def main(sender,recipients,subject,body,is_reminder,reminder_mails,reminder_numbers):
    
    global data
    chk_folder = Path('inbox_attachment_dir')
    if(chk_folder.is_dir()):
        print("The  folder is available")
    else:
        print("The folder is not available")


    gmail_password = 'shreyatej93'
    #recipients = ['chavanrachit16e@student.mes.ac.in','guptaabmeit16e@student.mes.ac.in','tejas.choudhari15@outlook.com','abygpta@gmail.com']

    email_sent = dbcreate()
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = subject
    
    outer['From'] = sender
    outer['Message-ID'] = email.utils.make_msgid()
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'
    
    
    # List of attachments
    attachments = []
    attachments_folder_name = subject+str(outer['Message-ID'])
    # Add the attachments to the message
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise

        '''
        try:
            with open(file,'rb') as fp:
        '''

    

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            for recipient in recipients:
                outer['To'] = recipient
                outer.attach(MIMEText(body, "html"))
                composed = outer.as_string()

                s.sendmail(sender, recipient, composed)
                del(outer['To'])
            s.close()
        print("Email sent!")
        #re = datetime.datetime.now() + datetime.timedelta(minutes=1)
        #re = re.timestamp()*1000
        email_sent.insert_one(
            {
                'to':recipients,
                'from':sender,
                'subject':outer['Subject'],
                'MessageID':str(outer['Message-ID']),
                'DateTime':datetime.datetime.now(),
                'time':time.time(),
                'attachments':attachments,
                'message':body,
                #'reminder':re,
                'reminder':data,
                'reminder_mails':reminder_mails,
                'reminder_numbers':reminder_numbers,
                'is_reminder':is_reminder
            }
        )

    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise

if __name__ == '__main__':
    main(sender,recipients,subject,body,is_reminder,reminder_mails,reminder_numbers)
    
    
