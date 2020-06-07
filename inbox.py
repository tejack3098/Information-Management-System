import sys
import imaplib
import getpass
import time
import email
import email.header
import datetime
import os
import pymongo
import re
EMAIL_ACCOUNT = "foodwastagemanger@gmail.com"
EMAIL_PASSWORD = 'shreyatej93'

# Use 'INBOX' to read inbox.  Note that whatever folder is specified,
# after successfully running this script all emails in that folder
# will be marked as read.
EMAIL_FOLDER = "your_attachment_dir"
M = None
inbox_dict=[]
email_sent,email_inbox=None,None

def dbcreate():
    global email_sent,email_inbox
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
        email_inbox = emaildb["emails_inbox"]
        emaildb.drop_collection(email_inbox)
        email_inbox = emaildb["emails_inbox"]
        email_inbox.insert_one({'Date_Created':now.isoformat()})
    return email_sent, email_inbox



def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None,True).decode("utf-8")

def get_attachments(msg):
    for part in msg.walk():
        if part.get_content_maintype()=='multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()

        if bool(fileName):
            filePath = os.path.join(EMAIL_FOLDER, fileName)
            with open(filePath,'wb') as f:
                f.write(part.get_payload(decode=True))

def has_attachments(msg):
    for part in msg.walk():
        if part.get_content_maintype()=='multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()

        if bool(fileName):
            return 1
        else:
            return 0

def get_attachments_now(msgID):
    typ, data = M.search(None, '(HEADER Message-ID "%s")' % msgID)
    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')

        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])
        get_attachments(msg)


def process_mailbox(M):
    """
    Do something with emails messages in the folder.
    For the sake of this example, print some headers.
    """

    global inbox_dict
    email_sent, email_inbox = dbcreate()
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return

    for num in data[0].split():

        curr_email = {}
        rv, data = M.fetch(num, '(RFC822)')

        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])


        hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
        frm = email.header.make_header(email.header.decode_header(msg['From']))

        messageID = email.header.make_header(email.header.decode_header(msg['Message-ID']))
        try:
            inReply = email.header.make_header(email.header.decode_header(msg['In-Reply-To']))
        except:
            inReply="NaN"



        msgContent = get_body(msg)
        #print(msgContent)


        subject = str(hdr)
        FRM = str(frm)
        msgID =str(messageID)
        #print('Suggest : ' + subject)
        #print('FROM : '+FRM)
        #print("inReply :  "+str(inReply))
        #print('Raw Date :', msg['Date'])
        #print('MessageID :'+msgID)
        #print(type(msgID))

        if(has_attachments(msg)==1):
            #print("ATTACHMENTS FOUND \n \t Getting them")
            #get_attachments_now(msgID)
            pass

        else:
            pass
            #print("No Attachments found")

        # Now convert to local date-time
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            #print ("Local Date:",local_date.strftime("%a, %d %b %Y %H:%M:%S"))
            print(local_date,"fhafsdhgasfdhf",local_date.timestamp()*1000)

        email_inbox.insert_one(
                {
                    'from':FRM,
                    'subject':subject,
                    'date':local_date,
                    'reply_time':local_date.timestamp()*1000,
                    'message':msgContent,
                    'hasAttachments':has_attachments(msg),
                    'inReply':str(inReply),
                    'messageID':msgID
                }
            )
        curr_email = {
                    'ID':msgID,
                    'data':{
                        'from':FRM,
                        'subject':subject,
                        'date':local_date,
                        'message':msgContent,
                        'hasAttachments':has_attachments(msg),
                        'inReply':str(inReply)
                        }
                }
        inbox_dict.append(curr_email)




def main():
    global M,inbox_dict

    M = imaplib.IMAP4_SSL('imap.gmail.com')


    try:
        rv, data = M.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    except imaplib.IMAP4.error:
        #print ("LOGIN FAILED!!! ")
        sys.exit(1)

    #print(rv, data)

    rv, mailboxes = M.list()
    if rv == 'OK':
        #print("Mailboxes:")
        #print(mailboxes)
        pass

    rv, data = M.select("INBOX")
    if rv == 'OK':
        #print("Processing mailbox...\n")
        process_mailbox(M)

        M.close()

    else:
        print("ERROR: Unable to open mailbox ", rv)


    M.logout()
    #print(inbox_dict)
    print("KKKKK\n\n\n\n\n\n\n",inbox_dict[0])
    return inbox_dict

if __name__ == '__main__':
    main()
