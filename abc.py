from flask import Flask, render_template
import json,csv
import random
from random import randint
app = Flask(__name__)

@app.route('/analytics')
def analytics():
        with open('ml/personlist.csv') as File:
                reader = csv.reader(File)
                s = set([row[0] for row in reader])
                
                option_list=[x for x in  s]
                department_list=['select','Ministry of Agriculture','Ministry of Chemicals and Fertilizers','Ministry of Civil Aviation External','Ministry of Coal External','Ministry of Commerce and Industry','Ministry of Communications and Information Technology','"Ministry of Consumer Affairs',' Food and Public Distribution External"','Ministry of Corporate Affairs External','Ministry of Culture External','Ministry of Defence External','Ministry of Development of North Eastern Region External','Ministry of Earth Sciences External','Ministry of Environment and Forests External','Ministry of External Affairs External','Ministry of Finance External','Ministry of Food Processing Industries External','Ministry of Health and Family Welfare External','Ministry of Heavy Industries and Public Enterprises','Ministry of Home Affairs External','Ministry of Housing and Urban Poverty Alleviation External','Ministry of Human Resource Development External','Ministry of Information and Broadcasting External','Ministry of Labour and Employment External','Ministry of Law and Justice External','"Ministry of Micro',' Small and Medium Enterprises External"','Ministry of Mines External','Ministry of Minority Affairs External','Ministry of New and Renewable Energy External','Ministry of Overseas Indian Affairs External','Ministry of Panchayati Raj External','Ministry of Parliamentary Affairs External','"Ministry of Personnel',' Public Grievances and Pensions External"','Ministry of Petroleum and Natural Gas External','Ministry of Power External','Ministry of Railways External','Ministry of Rural Development External','Ministry of Science and Technology','"Ministry of Shipping',' Road Transport and Highways"','Ministry of Social Justice and Empowerment External','Ministry of Statistics and Programme Implementation External','Ministry of Steel External','Ministry of Textiles External','Ministry of Tourism External','Ministry of Tribal Affairs External','Ministry of Urban Development External','Ministry of Water Resources External','Ministry of Women and Child Development External','Ministry of Youth Affairs and Sports External','Department of Atomic Energy External','Department of Space','Department of Information Technology (DIT)','Department of Post','Department of Telecommunications (DOT)']
                year_list=['2016q1','2016q2','2016q3','2016q4','2017q1','2017q2','2017q3','2017q4','2018q1','2018q2','2018q3','2018q4']

        return render_template('analysis.html',option_list=option_list,department_list=department_list,year_list=year_list)


@app.route('/analytics/user/<username>/<year>')
def analytics_name(username,year):
        with open('ml/personlist.csv') as File:
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
        with open('ml/we.csv',encoding='utf-8') as File:  
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


if __name__ == '__main__':
        app.run(debug = True)
