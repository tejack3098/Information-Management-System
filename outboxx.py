import sys

import time
import email
import email.header
import datetime
import os
import pymongo
import re


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

def main():
    all_out=[]
    email_sent,email_inbox=dbcreate()
    no_replies_email_id=[]
    for x in email_sent.find({"subject":{"$exists":True},'is_reminder':0}):
        msgID= x['subject']
        sub = "Re: "+x['subject']
        for i in x['reminder']:
            no_replies_dict=[]
            mail = i["id"]
            query2 = {"subject": {"$exists": True},"from":mail,'inReply':msgID, "subject": sub}
            chk = email_inbox.find_one(query2)
            '''
            print("CHK VALUE")
            print(chk)
            time.sleep(15)
            '''
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
        sout={
            "id":x['MessageID'],
            "data":{
                "from":x['from'],
                'subject':x['subject'],
                'DateTime':x['DateTime'],
                'reminder':x['reminder'],
                'replies':replies_email_id,
                'no_replies':no_replies_email_id,
                'count_replies':len(replies_email_id),
                'count_no_replies':len(no_replies_email_id)
            }

        }
        all_out.append(sout)
    print(all_out)
    return all_out

if __name__ == '__main__':
    main()
