from flask import Flask, request, jsonify
from flask import Flask,render_template,url_for,redirect
import requests
from requests.auth import HTTPBasicAuth
import json
import base64
import traceback
from datetime import datetime



app = Flask(__name__)

@app.route('/indexi')
def indexi():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/postLog')
def postLog():
    return render_template('postLog.html')

@app.route('/postWork')
def postWork():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            key=request.form['issueKey']
            comment='Testing 3'
            message = "VaibhavB2:Druv@family#21"
            message_bytes = message.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)

            base64_message = base64_bytes.decode('ascii')

            print(base64_message)
            print(key)

            url = "https://jira.verifone.com/rest/api/2/issue/"+key+"/worklog"

            #auth = HTTPBasicAuth("thesimpleguy03@gmail.com", "DW6fA0f8avNxLBNKVELa94C4")
            print(url)

            headers = {
            "Authorization": "Basic VmFpYmhhdkIyOkRydXZAZmFtaWx5IzIx",
            "Accept": "application/json",
            "Content-Type": "application/json"
            }

            payload = json.dumps( {
            "timeSpentSeconds": 1905,
            "comment":"Testing4",
            "started": "2021-01-20T06:40:40.885+0000"
            } )

            response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers
            )
            print(response)
    except:
        return jsonify({'trace': traceback.format_exc()})
    return render_template('postWork.html')

@app.route('/',methods=['GET','POST'])
def index():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            key = request.form.getlist('key[]')
            comment = request.form.getlist('comment[]')
            timeSpent = request.form.getlist('timeSpent[]')
            date = request.form.getlist('date[]')

            #message = "VaibhavB2:Druv@family#21"
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
            #r = datetime.datetime(2018, 9, 15)
            #print(r.strftime("%b %d %Y %H:%M:%S"))
            for a,b,c,d in zip(key,comment,timeSpent,date):
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
                payload = json.dumps( {
                "timeSpentSeconds": c,
                "comment":b,
                "started":d+":00.065+0000"
                } )
                response = requests.request(
                "POST",
                url,
                data=payload,
                headers=headers
                )
                print(payload)
                print(response.status_code)
            #nt=response.status_code
    except:
        return jsonify({'trace': traceback.format_exc()})

    return render_template('index.html')


@app.route('/getWorklog',methods=['GET','POST'])
def getWorklog():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            key=request.form['issueKey']

            message = "VaibhavB2:Druv@family#21"
            message_bytes = message.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)

            base64_message = base64_bytes.decode('ascii')

            print(base64_message)
            print(key)

            url = "https://jira.verifone.com/rest/api/2/issue/"+key+"/worklog"

            #auth = HTTPBasicAuth("thesimpleguy03@gmail.com", "DW6fA0f8avNxLBNKVELa94C4")
            print(url)

            headers = {
            "Authorization": "Basic VmFpYmhhdkIyOkRydXZAZmFtaWx5IzIx",
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

    return render_template('index.html',nt=t,key=key)



if __name__ == "__main__":
    print("App Runs")
    app.run(debug=True)