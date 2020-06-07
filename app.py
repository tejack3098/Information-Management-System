from flask import Flask, render_template, redirect, session,  url_for, escape, request, flash, send_from_directory
import json
from mailsend2 import *
from inbox import *
import datetime
import re
import time
from flask_ckeditor import CKEditor
import json,csv
import random
from random import randint
from docs2 import mainViewmail
from outbox import *

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 400
app.config['fullPage']=True


UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.secret_key="abcdffgdefgac"

ckeditor = CKEditor(app)


listt={
    "CSO":{
        "Director General":["sahilkadu12@gmail.com","abygpta@gmail.com"]
    },
    "PI wing":{
        "MPLADS":["tejas.choudhari10@gmail.com","rahulchavan220799@gmail.com"]
    }
    
}

def getPassword(username):
    if username=="admin":
        return "123"
    else:
        return "-1-1-1-1-1-1"
 
@app.route("/")
def welcome():
    if 'username' in session:
        return redirect(url_for('dashboard_inbox'))
    return redirect(url_for("login"))

@app.route("/login", methods=["get","post"])
def login():
    if request.method == 'POST':
        if request.form['password'] == getPassword(request.form['username']):
            session['username'] = request.form['username']
            return redirect(url_for('dashboard_compose'))
        else:
            flash('Incorrect Password and Username')
            return redirect(url_for("login"))
        ##Implement flash
    return render_template("home.html")

@app.route("/register",methods=["get","post"])
def register():
    if request.method=="POST":
        form=request.form
        username=form["username"]
        password=form["password"]
        mobile_number=form["mobile_number"]
        otp=form["otp"]
        email_id=form["email_id"]
        email_otp=form["email_otp"]
        print(username,password,mobile_number,otp,email_id,email_otp)
        
        return redirect(url_for("login"))
    else:
        return render_template("registration.html")
    
        

@app.route("/dashboard/compose",methods=["POST","GET"])
def dashboard_compose():
    
    print(request.method)
    #response.headers['Cache-Control'] = 'no-cache'
    if request.method=="POST":

        
        
        form=request.form
        '''for x in form:
            print(x)
            print(form[x])
        print(form)'''
        
        subject = form["subject"]
        try:
            email_id = form["email_id"]
        except:
            email_id = "-1"
        message = form["ckeditor"]
        attachments = form["attachments"]
        signature = form["signature"]
        gender = form["gender"]
        
        if(gender == "male"):
            
            dic = []
            for i in range(len(email_id.split(","))):
                
                remsg = "remsg"+str(i)
                remdate = "remdate"+str(i)
                remtime = "remtime"+str(i)
                remsms = "remsms"+str(i)
                print(remsg,remdate,remtime,remsms)
                data = {}
                data["id"]=email_id.split(",")[i]
                for x in form:
                    if remsg in x:
                        data["remsg"]=form[remsg]
                        #remsgFlag = True
                    if remdate in x:
                        data["remdate"]=form[remdate]
                        #remDateFlag = True
                    if remtime in x:
                        data["remtime"] = form[remtime]
                        #remTimeFlag = True
                    if remsms in x:
                        data["remsms"] = form[remsms]
                        #remsmsFlag = True
                s = data["remdate"]+" "+ data["remtime"]
                data["timestamp"] = time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M").timetuple())*1000
                '''data = {
                    
                    "remmsg":form[remsg],
                    "remdate":form[remdate],
                    "remtime":form[remtime],
                    "remsms":form[remsms]
                }'''

                #print(data)
                dic.append(data)
                
            print(dic)
            
        else:
            subsubdept = form["subsubdept"]
            
        
        if email_id== "-1":
            sendMailRonak(subject,subsubdept,message)
        else:
            sendMailRonak(subject,email_id,message,dic)
        
        #return "dic"
        return redirect(url_for("dashboard_inbox"))
            
        #send_mail=abhay_code.execute_smtp()
    else:
        if 'username' in session:
            user= session["username"]
            return render_template("compose_mail.html", user=user, department=[i for i in listt])
        else:
            return redirect(url_for("login"))

@app.route("/dashboard/inbox")
def dashboard_inbox():
    #response.headers['Cache-Control'] = 'no-cache'
    if 'username' in session:
        #data=abhay_code.execute_imap()
        data=main()
        user= session["username"]
        return render_template("inbox.html", user=user, data=data)
    else:
        return redirect(url_for("login"))

    
@app.route("/dashboard/mail_status")
def dashboard_mail_status():
    
    
    #response.headers['Cache-Control'] = 'no-cache'
    if 'username' in session:
        user= session["username"]
        data=main_outbox()
        return render_template("mail_status.html",data=data, user=user, department=[i for i in listt])
    else:
        return redirect(url_for("login"))
    
"""@app.route("/dashboard/analytics")
def dashboard_analytics():
    #response.headers['Cache-Control'] = 'no-cache'
    if 'username' in session:
        user= session["username"]
        return render_template("analytics.html", user=user, department=["A","B","C"])
    else:
        return redirect(url_for("login"))
"""
    
    
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/search")
def search():
    if 'username' in session:
        #execute search
        return render_template("search.html")
    else:
        return redirect(url_for("login"))
    
@app.route("/getdataSubDept/<dept>")
def getdataSubDept(dept):
    response=""
    #subdept=[dept+"1",dept+"2",dept+"3"]
    subdept=[i for i in listt[dept] ]
    
    
    for i in subdept:
        response+="<option>"+i+"</option>"
    return response

@app.route("/getdataSubSubDept/<dept>")
def getdataSubSubDept(dept):
    response=""
    subdept=[]
    for i in listt:
        if dept in listt[i]:
            subdept=listt[i][dept]
    
    for i in subdept:
        response+="<option>"+i+"</option>"
    return response
'''
@app.route('/dashboard/analytics')
def analytics():
   option_list=['select','rahul','tejas','sahil','ronak','abhay']
   department_list=['select','statistics','textiles']
   
   return render_template('analysis.html',option_list=option_list,department_list=department_list)


@app.route('/analytics/user/<username>')
def analytics_name(username):
   udict=[('rahul',20,5,'statistics',8803456213,'abc@gmail.com'),('tejas',38,12,'textiles',9867345234,'xyz@gmail.com'),('sahil',50,13,'statistics',9988776645,'aabbcc@gmail.com'),('ronak',55,19,'textiles',5657598765,'zyyy@gmail.com'),('abhay',60,13,'statistics',6767667895,'aaa@gamil.com')]
   for x in udict:
         if x[0] == username:
            d={"name":x[0],"regu":x[1],"reg":x[2],"dept":x[3],"cont":x[4],"email":x[5]}
            return json.dumps(d)


@app.route('/analytics/department/<departmentname>')
def department_name(departmentname):
   udict=[('statistics',27,6,4678765345,'anh@gamil.com'),('textiles',34,6,5675478447,'aaa@gmail.com')]
   for x in udict:
         if x[0] == departmentname:
            d={"name":x[0],"regu":x[1],"reg":x[2],"cont":x[3],"email":x[4]}
            return json.dumps(d) 

'''
        
@app.route('/enteremail')
def enteremail():
    return render_template('enteremail.html')

@app.route('/doc')
def document():
    return render_template('document.html')



@app.route('/analytics')
def analytics():
        with open('personlist.csv') as File:
                reader = csv.reader(File)
                s = set([row[0] for row in reader])
                
                option_list=[x for x in  s]
                department_list=['select','Ministry of Agriculture','Ministry of Chemicals and Fertilizers','Ministry of Civil Aviation External','Ministry of Coal External','Ministry of Commerce and Industry','Ministry of Communications and Information Technology','"Ministry of Consumer Affairs',' Food and Public Distribution External"','Ministry of Corporate Affairs External','Ministry of Culture External','Ministry of Defence External','Ministry of Development of North Eastern Region External','Ministry of Earth Sciences External','Ministry of Environment and Forests External','Ministry of External Affairs External','Ministry of Finance External','Ministry of Food Processing Industries External','Ministry of Health and Family Welfare External','Ministry of Heavy Industries and Public Enterprises','Ministry of Home Affairs External','Ministry of Housing and Urban Poverty Alleviation External','Ministry of Human Resource Development External','Ministry of Information and Broadcasting External','Ministry of Labour and Employment External','Ministry of Law and Justice External','"Ministry of Micro',' Small and Medium Enterprises External"','Ministry of Mines External','Ministry of Minority Affairs External','Ministry of New and Renewable Energy External','Ministry of Overseas Indian Affairs External','Ministry of Panchayati Raj External','Ministry of Parliamentary Affairs External','"Ministry of Personnel',' Public Grievances and Pensions External"','Ministry of Petroleum and Natural Gas External','Ministry of Power External','Ministry of Railways External','Ministry of Rural Development External','Ministry of Science and Technology','"Ministry of Shipping',' Road Transport and Highways"','Ministry of Social Justice and Empowerment External','Ministry of Statistics and Programme Implementation External','Ministry of Steel External','Ministry of Textiles External','Ministry of Tourism External','Ministry of Tribal Affairs External','Ministry of Urban Development External','Ministry of Water Resources External','Ministry of Women and Child Development External','Ministry of Youth Affairs and Sports External','Department of Atomic Energy External','Department of Space','Department of Information Technology (DIT)','Department of Post','Department of Telecommunications (DOT)']
                year_list=['2016q1','2016q2','2016q3','2016q4','2017q1','2017q2','2017q3','2017q4','2018q1','2018q2','2018q3','2018q4']

        return render_template('analysis.html',option_list=option_list,department_list=department_list,year_list=year_list)


@app.route('/analytics/user/<username>/<year>')
def analytics_name(username,year):
        with open('personlist.csv') as File:
                reader = csv.reader(File)
                names =[]
                reg = []
                delay = []
                for row in reader:
                        if username in row[0] and str(year.split("q")[0]) in row[7] and "q"+str(year.split("q")[1]) in row[8] :
                                print(row)
                                d={"name":row[0],"regu":row[1],"reg":row[2],"cont":row[6],"email":row[5],"design":row[4],"dept":row[3]}
                        if username in row[0] and str(year.split("q")[0]) in row[7]:
                                reg.append(row[1])
                                delay.append(row[2])
                d["regLL"] = reg
                d["delay"]=delay
                print (reg,delay)
                print(d)
                return json.dumps(d)
                



@app.route('/analytics/department/<departmentname>/<year>')
def department_name(departmentname,year):
        print(departmentname)
        with open('we.csv',encoding='utf-8') as File:  
                reader = csv.reader(File)
                names =[]
                reg = []
                delay = []

                for row in reader:

                        if departmentname in row[0] and str(year.split("q")[0]) in row[3] and "q"+str(year.split("q")[1]) in row[4] :
                                print(row)
                                d={"name":row[0],"regu":row[1],"reg":row[2],"cont":"".join(random.sample(['0','1','2','3','4','5','6','7','8','9'], 10)),"email":("".join(row[0][15:20])+"@gov.in").replace(" ","")}
                        if departmentname in row[0] and str(year.split("q")[0]) in row[3]:
                                reg.append(row[1])
                                delay.append(row[2])
                d["regLL"] = reg
                d["delay"]=delay
                print (reg,delay)
                print(d)
                return json.dumps(d)

@app.route('/getMailStatusData/<id>')
def getMailStatusData(id):
    data=mainViewmail(id)
    replyText=""
    c=1
    for i in data["replies"]:
        if i[3] is None:
            i[3]="None"
        replyText+="<h5 style='color: blue'>REPLY"+ str(c)+" BY:"+i[0]+"</h5> <p>"+i[2]+"</p><br>Attachments:"+str(i[3])
        if i[3]!="None":
            replyText+="<a href='../static/pdf.pdf' download>Download PDF.</a>" 
        replyText+="<br><br><hr>"
        c+=1
    print("replyText",replyText)
    return render_template('document.html',data=data,reply=replyText)

if __name__ == "__main__":
    app.run(debug=True)