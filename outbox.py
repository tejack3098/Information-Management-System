import pymongo
import datetime
import inbox
import re
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

def chk_no_replies():

    all_mails_dict=[]
    query = {"subject": {"$exists": True},"is_reminder":0}
    #print("LENGTH "+str(len(email_sent.find(query))))


    for x in email_sent.find(query):
        #print(x)
        #print("-------------------------------------")
        #print("SUBJECT: "+x['subject'])
        sub = "Re: "+x['subject']
        msgID = x['MessageID']
        replies = email_inbox.find({"subject": {"$exists": True},"subject": sub,'inReply':msgID})
        replies_email_id =[]
        no_replies_email_id=[]
        for reply in replies:

            #print('\t From:'+reply['from'])
            #print('\t \t Subject:'+reply['subject'])
            #print('\t \t Message:'+reply['message'])
            replies_email_id.append((re.findall(r'\<(.+?)\>',reply['from']))[0])

        #print("REPLIED IDs -->")
        #print(replies_email_id)
        no_replies_email_id =list(set(x['to'])-set(replies_email_id))
        #print("NOT REPLIED IDs -->")
        #print(no_replies_email_id)
        from datetime import datetime


        ekd={
            'id':x['_id'],
            'data':{
                'to':x['to'],
                'from':x['from'],
                'subject':x['subject'],
                'MessageID':x['MessageID'],
                'DateTime':x['DateTime'],
                'time':x['time'],
                'attachments':x['attachments'],
                'message':x['message'],
                'reminder':  x['reminder'],#abhay
                'reminder_mails':x['reminder_mails'],
                'reminder_numbers':x['reminder_numbers'],
                'is_reminder':x['is_reminder'],
                'no_replies':no_replies_email_id,
                'replies':replies_email_id,
                'num_no_replies':len(no_replies_email_id),
                'num_replies':len(replies_email_id)
                
            }

        }
        all_mails_dict.append(ekd)
    return all_mails_dict
    

def main_outbox():
    global email_sent,email_inbox
    email_sent,email_inbox = dbcreate()
    inbox.main() 
    all_mails=chk_no_replies()
                                 
    '''
    mails = email_sent.find({"subject":{"$exist":True}})
    for mail in mails:
        curr_mail={
            'to':mail['to'],
            'from':mail['from'],
            'subject':mail['subject],
            'MessageID':mail['MessageID],
            'DateTime':mail['DateTime'],
            'time':time,
            'attachments':mail['attachments'],
            'message':mail['message'],
            'reminder':mail['reminder'],
            'reminder_mails':mail['reminder_mails'],
            'reminder_numbers':mail['reminder_numbers'],
            'is_reminder':mail['is_reminder']
        }
        all_mails.append(curr_mail)
    '''
    
    return all_mails
#print(main_outbox())
