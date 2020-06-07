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
no_replies_dict=[]
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
def process_mailbox(M,no_replies_dict):
    """
    Do something with emails messages in the folder.
    For the sake of this example, print some headers.
    """

    global email_sent, email_inbox
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return

    for num in data[0].split():

        rv, data = M.fetch(num, '(RFC822)')

        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])


        hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
        frm = email.header.make_header(email.header.decode_header(msg['From']))
        frm = str(frm)
        frm = (re.findall(r'\<(.+?)\>',frm))[0]
         
        messageID = email.header.make_header(email.header.decode_header(msg['Message-ID']))
        try:
            inReply = email.header.make_header(email.header.decode_header(msg['In-Reply-To']))
        except:
            inReply="No IN-REPLY"

        print('-------------------------------------')
        print("MESSAGE ---> ")

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

        msgContent = get_body(msg)
        #print(msgContent)

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        subject = str(hdr)
        FRM = str(frm)
        msgID =str(messageID)
        print('Suggest : ' + subject)
        print('FROM : '+FRM)
        print("inReply :  "+str(inReply))
        print('Raw Date :', msg['Date'])
        print('MessageID :'+msgID)
        print(type(msgID))
        print('++++++++++++++++++++++++++++++++++++++++')
        if(has_attachments(msg)==1):
            print("ATTACHMENTS FOUND \n \t Getting them")
            #get_attachments_now(msgID)

        else:
            print("No Attachments found")
        print('++++++++++++++++++++++++++++++++++++++++')
        # Now convert to local date-time
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            print ("Local Date:", \
                local_date.strftime("%a, %d %b %Y %H:%M:%S"))
        print('-------------------------------------')
        print('\n \n')

        email_inbox.insert_one(
                {
                    'from':FRM,
                    'subject':subject,
                    'date':local_date,
                    'message':msgContent,
                    'hasAttachments':has_attachments(msg),
                    'inReply':str(inReply),
                    'messageID':msgID
                }
            )
    chk_no_replies(no_replies_dict)


def chk_no_replies(no_replies_dict):

    query = {"subject": {"$exists": True},"is_reminder":0}
    #print("LENGTH "+str(len(email_sent.find(query))))


    for x in email_sent.find(query):
        print(x)
        print("-------------------------------------")
        print("SUBJECT: "+x['subject'])
        sub = "Re: "+x['subject']
        msgID = x['MessageID']
        no_replies_email_id=[]
        for i in x['reminder']:
            
            mail = i["id"]
            query2 = {"subject": {"$exists": True},"from":mail,'inReply':msgID, "subject": sub}
            chk = email_inbox.find_one(query2)
            print("CHK VALUE")
            print(chk)
            time.sleep(15)
            if chk == None:
                no_replies_dict.append({'id':mail,'remtime':i['remtime'],'remdate':i['remdate'],\
                                       'remsg':i['remsg'],'remsms':i['remsms'],'timestamp':i['timestamp'],\
                                       'subject':x['subject'],'sentDate':x['DateTime'],\
                                      'remnumbers':x['reminder_numbers']})
                no_replies_email_id.append(mail)
                   
            
        #replies = email_inbox.find({"subject": {"$exists": True},"subject": sub,'inReply':msgID})
        replies_email_id =[]
        '''
        for reply in replies:

            print('\t From:'+reply['from'])
            print('\t \t Subject:'+reply['subject'])
            print('\t \t Message:'+reply['message'])
            replies_email_id.append((re.findall(r'\<(.+?)\>',reply['from']))[0])
        '''
        
        replies_email_id =list(set((x['to'][0]).split(','))-set(no_replies_email_id))
        print("REPLIED IDs -->")
        print(replies_email_id)
        print("NOT REPLIED IDs -->")
        print(no_replies_email_id)

        '''
        ekd={
            'id':x['_id'],
            'data':{
                'subject':x['subject'],
                'reminder':x['reminder'],
                'DateTime':x['DateTime'],
                'no_replies':no_replies_email_id,
                'reminder_mails':x['reminder_mails'],
                'reminder_numbers':x['reminder_numbers']
            }

        }
        
        no_replies_dict.append(ekd)
        '''
    print("NO REPLY DETAILS \n \t",no_replies_dict)
    print(len(no_replies_dict))

def main():
    global M,no_replies_dict,start,email_sent, email_inbox
    email_sent, email_inbox = dbcreate()
    M = imaplib.IMAP4_SSL('imap.gmail.com')

    no_replies_dict=[]

    try:
        rv, data = M.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    except imaplib.IMAP4.error:
        print ("LOGIN FAILED!!! ")
        sys.exit(1)

    print(rv, data)

    rv, mailboxes = M.list()
    if rv == 'OK':
        print("Mailboxes:")
        print(mailboxes)

    rv, data = M.select("INBOX")
    if rv == 'OK':
        print("Processing mailbox...\n")
        process_mailbox(M,no_replies_dict)
        #print("Its sleep time")
        #time.sleep(15)

        #process_mailbox(M,no_replies_dict)
        M.close()

    else:
        print("ERROR: Unable to open mailbox ", rv)

    '''
    rv, mailboxes = M.list()
    if rv == 'OK':
        print("Mailboxes:")
        print(mailboxes)

    rv, data = M.select("INBOX")
    if rv == 'OK':
        print("Processing mailbox...\n")
        process_mailbox(M,no_replies_dict)
    '''

    M.logout()
    return no_replies_dict
if __name__ == '__main__':
    main()
