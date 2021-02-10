from flask import Flask, request, jsonify
from flask import Flask,render_template,url_for,redirect
import requests
from requests.auth import HTTPBasicAuth
import json
import base64
import traceback
from datetime import datetime
import webbrowser



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/errors')
def errors():
    return render_template('error.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/getDashboard')
def getDashboard():
    try:
        url = "https://jira.verifone.com/rest/api/2/dashboard/33333"

        #auth = HTTPBasicAuth("email@example.com", "<api_token>")

        headers = {
            "Authorization": "Basic ###############",
            "Accept": "application/json"
        }
        url1="https://jira.verifone.com/secure/Dashboard.jspa?selectPageId=33333"
        webbrowser.open_new_tab(url1)
        
    except:
        return jsonify({'trace': traceback.format_exc()})
    return render_template('index.html')
    

#POST WORK LOG------------------------------------------------------------
@app.route('/postWorklog',methods=['GET','POST'])
def postWorklog():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            key = request.form.getlist('key[]')
            comment = request.form.getlist('comment[]')
            timeSpent = request.form.getlist('timeSpent[]')
            date = request.form.getlist('date[]')
            key1=key[1:]
            comment1=comment[1:]
            timeSpent1=timeSpent[1:]
            date1=date[1:]
            message = username+":"+password
            message_bytes = message.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            base64_message = base64_bytes.decode('ascii')

            print(base64_message)
            print(key)
            print(comment)
            print(timeSpent)
            print(date)

            m=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print(m)

            tSpent = []
            for j in timeSpent:
                j="".join(j.split()).lower()
                l1=[]
                m1=[]
                r=True
                s1=""
                for i in j:
                    if i.isalpha() and r==False:
                        m1.append(i)
                        k1=int(s1)
                        l1.append(k1)
                        r=True
                        s1=""
                    elif i.isdigit():
                        s1+=i
                        r=False
                    elif i.isalpha() and r==True:
                        s+='0'
                        k=int(s)
                        m.append(i)
                        l1.append(k)
                        s=""    
                t1=0
                for x1,y1 in zip(m1,l1):
                    if x1=='w':
                        q1=5*8*60*60*y1
                        t1+=q1
                    elif x1=='d':
                        v1=8*60*60*y1
                        t1+=v1
                    elif x1=='h':
                        u1=60*60*y1
                        t1+=u1
                    elif x1=='m':
                        f1=y1*60
                        t1+=f1
                    elif x1=='s':
                        t1+=y1
                tSpent.append(t1)

            for a,b,c,d in zip(key,comment,tSpent,date):
                url = "https://jira.verifone.com/rest/api/2/issue/"+a+"/worklog"
                headers = {
                "Authorization": "Basic "+base64_message,
                "Accept": "application/json",
                "Content-Type": "application/json"
                }
                print(a)
                print(b)
                print(c)
                print(d)
                date_time_obj = datetime.strptime(d,'%Y:%m:%d %H:%M:%S.%f').isoformat()
                print(date_time_obj[:-3])
                date_time_obj = date_time_obj[:-3]
                payload = json.dumps( {
                "timeSpentSeconds": c,
                "comment":b,
                "started":date_time_obj+"+0000"
                } )
                response = requests.request(
                "POST",
                url,
                data=payload,
                headers=headers
                )
                en1=response.status_code
                print(en1)
                now = datetime.now()
                now_time = now.strftime("%b-%d-%Y %H:%M:%S")
                print(now_time)
        else:
            return render_template('error.html')    
    except:
        return jsonify({'trace': traceback.format_exc()})

    return render_template('index.html',user=username,n_time=now_time,ent=en1,keys=key,comments=comment,timeSpents=timeSpent,dates=date,fol=zip(key1,comment1,timeSpent1,date1))

##TESTING CODE -------------------------------------------------------------------------------------------
'''
@app.route('/postWorklog',methods=['GET','POST'])
def postWorklog():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            key = request.form.getlist('key[]')
            comment = request.form.getlist('comment[]')
            timeSpent = request.form.getlist('timeSpent[]')
            date = request.form.getlist('date[]')
            message = username+":"+password
            message_bytes = message.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            base64_message = base64_bytes.decode('ascii')
            print(key)
            print(comment)
            print(timeSpent)
            print(date)
            key1=key[1:]
            comment1=comment[1:]
            timeSpent1=timeSpent[1:]
            date1=date[1:]
            en1=201
            print(en1)
            now = datetime.now()
            now_time = now.strftime("%b-%d-%Y %H:%M:%S")
            print(now_time)
        else:
            return render_template('error.html')
    except:
        return jsonify({'trace': traceback.format_exc()})

    return render_template('index.html',user=username,n_time=now_time,ent=en1,keys=key,comments=comment,timeSpents=timeSpent,dates=date,fol=zip(key1,comment1,timeSpent1,date1))

'''

#Fetching Logs from JIRA------------------------------------------------------------------------

@app.route('/getWorklog',methods=['GET','POST'])
def getWorklog():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            key=request.form['issueKey']

            message = username+":"+password
            message_bytes = message.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)

            base64_message = base64_bytes.decode('ascii')

            print(base64_message)
            print(key)

            url = "https://jira.verifone.com/rest/api/2/issue/"+key+"/worklog"

            print(url)

            headers = {
            "Authorization": "Basic <api_access token>",
            "Accept": "application/json",
            "Content-Type": "application/json"
            }

            response = requests.request(
            "GET",
            url,
            headers=headers
            )
            #print(response)
            s= json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
            t = json.loads(s)
    except:
        return jsonify({'trace': traceback.format_exc()})

    return render_template('getLogs.html',nt=t,key=key)



if __name__ == "__main__":
    print("App Runs")
    app.run(debug=True)