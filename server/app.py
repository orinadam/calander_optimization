import os
import sys
import logging
import base64 
from load_files import loadFiles 
from extra_funcs import * 
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_session import Session
from flask_cors import CORS #comment this on deployment
import load_to_database as db
import make_schedule as ms
import datetime

UPLOAD_FOLDER = ''
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'super secret key'

sess = Session()
CORS(app) #comment this on deployment
app.config['CORS_HEADERS'] = 'Content-Type:multipart/form-data'


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#specific_candidate(first_name_candidate, family_name_candidate , schedule):
@app.route('/findspecific', methods=['POST', "GET"])
def send_specific():
    firstname = request.args.get('firstname')
    secondname =  request.args.get('secondname')
    res =  [["שם פסיכולוג", "שעת ראיון" ,"יום", "שם פרטי", "שם משפחה", "מ.א", "הערות","טלפון", "דפר", "שנות לימוד","סימול עברית", "מייל"  ,  "code"]]
    schedule = ms.make_schedule(db.get_candidates_list(0), db.get_psychologists_list(0))
    value = list(ms.to_excel(schedule, 0))
    del value[0]
    s = specific_candidate(firstname, secondname, value)
    isEmpty = "true" if s == None else "false"
    res.append(s)
    return {"data" : res, "error" : "", "isempty": isEmpty}



#def candidates_available_for_exchange(personal_number, schedule):
@app.route('/replacement', methods=['POST', "GET"])
def find_replacement():
    personal_number =  request.args.get('personnumber')
    value = list(loadFiles())
    del value[0]
    s = []#candidates_available_for_exchange(personal_number, value)
    print(len(s))
    isEmpty = "true" if len(s) < 1 else "false" #TODO: check this starnage one  liner fumcionality 

    return {"data" : s, "error" : "", "isempty": isEmpty}

@app.route('/check', methods=['POST', "GET"])
def send():
    search = request.args.get('data')
    schedule = ms.make_schedule(db.get_candidates_list(0), db.get_psychologists_list(0))
    value = list(ms.to_excel(schedule, 0))
    del value[0]
    s = same_psychologist(search, value)
    isEmpty = "true" if s == None else "false"
    return {"data" : s, "error" : "", "isempty": isEmpty}

@app.route('/luz', methods=['POST', "GET"])
def sned_authority():
    authority = request.args.get('authority')
    schedule = ms.make_schedule(db.get_candidates_list(0), db.get_psychologists_list(0))
    value = list(ms.to_excel(schedule, 0))
    del value[0]
    print(value)
    s = luz_authority(value, authority)
    isEmpty = "true" if s == None else "false"
    print(s)
    return {"data" : s, "error" : "", "isempty": isEmpty}

@app.route('/days', methods=['POST', "GET"])
def find_day():
    day = request.args.get('day')
    schedule = ms.make_schedule(db.get_candidates_list(0), db.get_psychologists_list(0))
    value = list(ms.to_excel(schedule, 0))
    del value[0]
    print(value)
    s = filter_by_day(value, day)
    isEmpty = "true" if s == None else "false"
    print(s)
    return {"data" : s, "error" : "", "isempty": isEmpty}


@app.route('/getstart', methods=['POST', "GET"])
def send_start():
    w1 = datetime.datetime(year=2022, month=1, day=1)
    schedule = ms.make_schedule(db.get_candidates_list(0), db.get_psychologists_list(0))
    value = list(ms.to_excel(schedule, 0))
    return {"data" : value, "error" : ""}

@app.route('/cleantable', methods=["GET"])
def clean_table():
    db.clear_meetings_table(0)
    db.clear_candidates_table(0)
    db.clear_psychologists_table(0)
    return {"data" : "value", "error" : ""}


@app.route('/deleteone', methods=[ "GET"])
def delete_candidate():
    code = request.args.get('code')
    db.remove_single_candidate(int(code), 0 )
    return {"data" : "value", "error" : ""}

@app.route('/', methods=['POST', "GET"])
def upload_file():
    filenames = [
    
      "candidates",
      "psychologists",
      "working_hours",
      "conditions",
      "candidates_conditions",
      "candidates_available_hours",
    ]

    app.logger.warning(request)
    if request.method == "GET":
        return "checking"
    if request.method == 'POST':
        for name in filenames:
            if name not in request.files:
                continue
            file = request.files[name]
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # connect to the database

    result = loadFiles()
    print(result)
    value = result[0]
    print("THIS IS THE REAL SCHDULE:")


        
    print(value)
    """
    value = [["candidate", "day", "hour", "psychologist", "id"],
            ["Maor", "Sunday", "12:00", "Guy", 1],
            ["Maor", "Sunday", "12:00", "Guy", 2],
            ["Maor", "Sunday", "12:00", "Guy", 3],
    ]
    """
    #str1 = ''.join(str(e) for e in value)
    # use the algorithm to send the schedule
    #return schedule
    #["error - invalid id", "this is another check", "test"]
    print(result[1])
    return {"data" : value, "error" : result[1]}


if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)
    app.run(debug=True, host="0.0.0.0")
