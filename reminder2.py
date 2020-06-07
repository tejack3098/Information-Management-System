import mailread6
import sms
from mailread6 import no_replies_dict
import mailsend2
import time
import datetime
import sched
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
COMMASPACE = ', '


s = sched.scheduler(time.time, time.sleep)

isPause = False;

reminder_mails=[None]
reminder_numbers=[None]

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
    print('Recipients --------> ')
    print(recipients)
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
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer['Message-ID'] = email.utils.make_msgid()
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'
    outer.attach(MIMEText(body, "plain"))
    print(outer['Message-ID'])

    print(type(outer['Message-ID']))

    print(str(outer['Message-ID']))

    print(type(str(outer['Message-ID'])))
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

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
        re = datetime.datetime.now() + datetime.timedelta(minutes=1)
        re = re.timestamp()*1000
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
                'reminder':re,
                'reminder_mails':reminder_mails,
                'reminder_numbers':reminder_numbers,
                'is_reminder':is_reminder
            }
        )

    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise


def reminder():
    global isPause
    if(isPause != True):
        isPause = True;
        no_replies_dict=mailread6.main()

        #print("NO REPLY DETAILS \n \t",no_replies_dict)
        print(len(no_replies_dict))



        for i in no_replies_dict:
            reminder = "This is a reminder for "+i['subject']

            #body = "This is reminder mail for the subject  "+i['data']['subject']+" sent on "+

            body=i['remsg']
            ID = i['id']
            re= i['timestamp']
            #eids=i['data']['no_replies']
            #print("eids:>>>>>>>>>>>>>>>>>>>>>>")
            #print(eids)
            '''
            for eid in eids:
                body = body+"  " + eid
            body = body + "  accounts. \n"
            body = body + "For the mail sent on "+str(i['data']['DateTime'])+" ."
            '''
            reminder_mails = ID
            print(" REMINDER MAILS "+str(reminder_mails))
            #time.sleep(30)
            reminder_numbers=i['remnumbers']
            currtime = datetime.datetime.now()
            currtime = currtime.timestamp()*1000
            if(currtime>re):
                main('foodwastagemanger@gmail.com',ID,reminder,body,1,reminder_mails,reminder_numbers)
                if i['remsms']=="yes":
                    print("SENDING SMS")
                    sms.main(reminder_numbers,body)

        isPause = False

def do_something(sc):
    #print ("Doing stuff...")
    # do your stuff
    reminder()
    s.enter(10, 1, do_something, (sc,))

s.enter(10, 1, do_something, (s,))
s.run()

