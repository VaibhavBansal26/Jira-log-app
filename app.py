from flask import Flask, request, jsonify
from flask import Flask,render_template,url_for,redirect
import requests
from requests.auth import HTTPBasicAuth
import json
import base64
import traceback
from datetime import datetime
from datetime import timezone
import pytz
from dateutil.tz import *
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
        return redirect(url1)
        
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
            rc=[]
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
                date_time_obj = datetime.strptime(d,'%Y:%m:%d %H:%M:%S.%f')
                print(str(date_time_obj)[:-3])
                local = tzlocal()
                date_time_obj = date_time_obj.replace(tzinfo = local)
                date_time_obj = date_time_obj.astimezone(local).isoformat()
                g1=str(date_time_obj)[-6:]
                g=str(date_time_obj)[:-9]
                g1=g1.replace(":","")
                g3=g+g1
                print(g3)
                print(date_time_obj)
                payload = json.dumps( {
                "timeSpentSeconds": c,
                "comment":b,
                "started":g3
                } )
                response = requests.request(
                "POST",
                url,
                data=payload,
                headers=headers
                )
                en1=response.status_code
                rc.append(en1)
                now=datetime.now()
                local = tzutc()
                now = now.replace(tzinfo = local)
                now_time = now.astimezone(local).strftime("%b-%d-%Y %H:%M:%S")
                print(now_time)
            print(rc)
            w=[]
            count=0
            for i in range(0,len(rc)-1):
                if rc[i] == 201:
                    count+=1
                else:
                    w.append(i+1)
            tot_q=len(rc)
            s_q=abs(len(rc)-len(w))
            uns_q=len(w)
            if 201 in rc:
                q=True
            else:
                q=False                
        else:
            return render_template('error.html')    
    except:
        return render_template('error.html')

    return render_template('index.html',res=q,rcs=rc,r_q=s_q,sq=tot_q,un_q=uns_q,cnt=count,ind=w,user=username,n_time=now_time,ent=en1,keys=key,comments=comment,timeSpents=timeSpent,dates=date,fol=zip(key1,comment1,timeSpent1,date1))

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
            d=date[0]
            d1=datetime.strptime(d,'%Y:%m:%d %H:%M:%S.%f')
            print(d1)
            now = datetime.now()
            now_time = now.strftime("%b-%d-%Y %H:%M:%S")
            print(now_time)
            local = tzlocal()
            now = now.replace(tzinfo = local)
            now = now.astimezone(local).isoformat()
            print(now)
            now1 = d1.replace(tzinfo = local)
            now1 = d1.astimezone(local).isoformat()
            print(now1)
            l=[401,401,401,401]
            w=[]
            count=0
            for i in range(0,len(l)-1):
                if l[i] == 201:
                    count+=1
                else:
                    w.append(i+1)
            tot_q=len(l)
            s_q=abs(len(l)-len(w))
            uns_q=len(w)
            if 201 in l:
                q=True
            else:
                q=False
        else:
            return render_template('error.html')
    except:
        return jsonify({'trace': traceback.format_exc()})

    return render_template('index.html',res=q,rcs=l,r_q=s_q,sq=tot_q,un_q=uns_q,cnt=count,ind=w,user=username,n_time=now_time,ent=en1,keys=key,comments=comment,timeSpents=timeSpent,dates=date,fol=zip(key1,comment1,timeSpent1,date1))


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