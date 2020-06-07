#import docx
#from wordcloud import WordCloud, STOPWORDS
#from docx.shared import Inches
#from docx.enum.dml import MSO_THEME_COLOR_INDEX
import re
import time
import sys
import pymongo
import imaplib
import email
import os
from pathlib import Path
#from gensim.summarization.summarizer import summarize
#from gensim.summarization import keywords
#import matplotlib.pyplot as plt
import requests
#import PyPDF2
global M
EMAIL_FOLDER = "your_attachment_dir"
WORD_MAP_FOLDER = "word_map"
EMAIL_ACCOUNT = "foodwastagemanger@gmail.com"
EMAIL_PASSWORD = 'shreyatej93'
M = None
#stopwords = set(STOPWORDS)
wordpath=""



"""

sum_all_pdf = []
sum_all_msg = []
sum_all_docx = []
sum_all_docx1 = []
sumdocx1 = " "
sumdocx2 = " "
sumpdf = " "
sumdocx = " "
summsg = " "
def pdfsummary(path,rmsgID):
    global WORD_MAP_FOLDER
    global MSGID,wordpath
    rmsgID=re.sub(r'\W+','', rmsgID)
    pdf_file = open(path, 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    a = []
    b = " "
    for i in range(number_of_pages):
        page = read_pdf.getPage(i)
        page_content = page.extractText()
        docs1 = page_content.encode('utf-8')
        docs = str(docs1)
        a.append(docs)


    b= ''.join(a)
    print(b)
    wordcloud = WordCloud(width=800, height=800, background_color = 'white', stopwords=stopwords, min_font_size=10).generate(b)
    plt.figure(figsize=(8,8),facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    wordpath = WORD_MAP_FOLDER+"/"+rmsgID+'.png'
    print("WORDPATH "+wordpath)
    time.sleep(30)
    wordcloud.to_file(wordpath)
    #print("Docs print ::::: ")
    #print (docs)
    a = summarize(b, word_count=200)
    sum_all_pdf.append(a)
    return a

def msgsummary(msg):
    #print(msg)
    print ('Summary:')
    sum_all_msg.append(msg)
    a=summarize(msg, ratio=0.25)
    print(a)
    #sum_all_msg.append(a)
    return a
def allpdfsummary(file):
    sumpdf1=sumpdf.join(file)
    print("Summary")
    print(summarize(sumpdf1, ratio=0.3))

def allmsgsummary(file):

    summsg1=summsg.join(file)
    #print(summsg1)
    print("Summary")
    print(summarize(summsg1, ratio=0.3))


def docxsummary(path,rmsgID):
    document = docx.Document(path)
    global WORD_MAP_FOLDER
    global MSGID,wordpath
    rmsgID=re.sub(r'\W+','', rmsgID)
    for para in document.paragraphs:
        print(para.text)
        sum_all_docx.append(para.text)

    sumdocx1 = sumdocx.join(sum_all_docx)
    print ('Summary:')
    sum_all_docx1.append(sumdocx1)
    wordcloud = WordCloud(width=800, height=800, background_color = 'white', stopwords=stopwords, min_font_size=10).generate(sumdocx1)
    plt.figure(figsize=(8,8),facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    wordpath = WORD_MAP_FOLDER+"/"+rmsgID+'.png'
    print("WORDPATH "+wordpath)
    time.sleep(30)
    wordcloud.to_file(wordpath)
    a=summarize(sumdocx1, ratio=0.25)

    print(a)
    return a
"""
"""def alldocxsummary(file):

    sumdocx2=sumdocx1.join(file)
    print("Summary")
    print(summarize(sumdocx2, ratio=0.3))
"""

def getDB():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    emaildb = myclient["EmailDB"]
    email_sent = emaildb["emails_sent"]
    email_inbox = emaildb["emails_inbox"]
    return email_sent,email_inbox

"""def get_attachments(msg,msgID,email_folder):
    file_links = []

    for part in msg.walk():
        if part.get_content_maintype()=='multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()

        if bool(fileName):
            #fileName = re.sub(r'\W+', '', fileName)
            fileName = re.sub(r'\W-_.', '', fileName)

            filePath = os.path.join(email_folder, fileName)

            filename, file_extension = os.path.splitext(filePath)
            print("File Extension : ")
            print(file_extension)
            with open(filePath,'wb') as f:
                f.write(part.get_payload(decode=True))


            if file_extension in ['.pdf','.txt','.docx']:
                print(" PDF TXT DOCX ")
                if(file_extension =='.pdf'):
                    print(" PDF ")
                    print(filePath)
                    docsumm=(pdfsummary(filePath,msgID))
                    print(docsumm)


                else:
                    print(" DOCX ")
                    docsumm=(docxsummary(filePath))
                print(" DOC SUM ")




                data={
                    'filePath':filePath,
                    'is_doc':1,
                    'summary':docsumm
                }
            else:
                data={
                    'filePath':filePath,
                    'is_doc':0
                }



            file_links.append(data)
    return file_links
"""
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
        '''
def get_attachments_now(msgID):
    global M,EMAIL_FOLDER
    typ, data = M.search(None, '(HEADER Message-ID "%s")' % msgID)
    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')

        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])

        '''
        msgID = msgID.replace("<","")
        msgID = msgID.replace(">","")
        '''
        msgID = re.sub(r'\W+', '', msgID)
        email_folder = EMAIL_FOLDER+"\\"+msgID
        default_path='C:\\Users\\Gupta Niwas\\Downloads\\Hackathon\\gmail\\'
        if(Path(default_path+email_folder).is_dir()):
            pass
        else:
            os.mkdir(default_path+email_folder)
        return(get_attachments(msg,msgID,email_folder))'''

"""def add_hyperlink(paragraph, text, url):
    # This gets access to the document.xml.rels file and gets a new relation id value
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    # Create the w:hyperlink tag and add needed values
    hyperlink = docx.oxml.shared.OxmlElement('w:hyperlink')
    hyperlink.set(docx.oxml.shared.qn('r:id'), r_id, )

    # Create a w:r element and a new w:rPr element
    new_run = docx.oxml.shared.OxmlElement('w:r')
    rPr = docx.oxml.shared.OxmlElement('w:rPr')

    # Join all the xml elements together add add the required text to the w:r element
    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)

    # Create a new Run object and add the hyperlink into it
    r = paragraph.add_run ()
    r._r.append (hyperlink)

    # A workaround for the lack of a hyperlink style (doesn't go purple after using the link)
    # Delete this if using a template that has the hyperlink style in it
    r.font.color.theme_color = MSO_THEME_COLOR_INDEX.HYPERLINK
    r.font.underline = True

    return hyperlink


"""
def mainViewmail(msgID):
    global M
    global MSGID,wordpath
    MSGID = msgID
    M = imaplib.IMAP4_SSL('imap.gmail.com')
    D = {}

    try:
        rv, data = M.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    except imaplib.IMAP4.error:
        print ("LOGIN FAILED!!! ")
        sys.exit(1)
    rv, mailboxes = M.list()


    rv, data = M.select("INBOX")
    email_sent,email_inbox = getDB()
    #doc_file = docx.Document()
    sent_mail = email_sent.find_one({"subject":{"$exists":True},"MessageID":msgID})
    msg = sent_mail['message']
    subject = sent_mail['subject']
    D["msg"]=msg
    D["subject"]=subject
    

    #doc_file.add_heading(" SUBJECT : "+subject)
    #doc_file.add_paragraph(" MESSAGE "+msg)
    #doc_file.add_heading(" REPLIES ")
  
    subject = "Re: "+subject
    replies = email_inbox.find({"subject": {"$exists": True},"subject": subject,'inReply':msgID})
    #i=1
    #print(len(replies))
    reply_list=[]
    for reply in replies:
        fromm=reply['from']
        msgID = reply['messageID']
        msgContent = reply['message']
        hasAttachment=reply['hasAttachments']
        reply_list.append([fromm,msgID,msgContent,hasAttachment])
    D['replies']=reply_list
    #for reply in replies:
        #doc_file.add_heading(" Reply"+str(i))
        #frm = reply['from']
        #msgID = reply['messageID']
        #msgContent = reply['message']
        #print("FROM "+frm)
        #print("MESSAGE CONTENT "+msgContent)
        #doc_file.add_heading("REPLY BY: "+frm)
        #doc_file.add_paragraph(" IN MAIL DETAILS "+msgContent)

        #if(reply['hasAttachments']!=None):
            #p=doc_file.add_paragraph(" ATTACHMENTS \n")
            #file_links = get_attachments_now(msgID)
            #for file_link in file_links:
                #add_hyperlink(p, ' Click here to see attachment \n', file_link['filePath'])
                #if(file_link['is_doc'] and len(file_link['summary'])!=0):
                    #doc_file.add_picture(wordpath, width=Inches(1.24))
                    #doc_file.add_heading('\t SUMMARY')
                    #doc_file.add_paragraph(file_link['summary'])

        #print('\t \t Subject:'+reply['subject'])
        #i=i+1
    return D