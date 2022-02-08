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



UPLOAD_FOLDER = ''
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'super secret key'

sess = Session()
CORS(app) #comment this on deployment
app.config['CORS_HEADERS'] = 'Content-Type:multipart/form-data'


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/check', methods=['POST', "GET"])
def send():
    value = list(loadFiles())
    del value[0]
    s = same_psychologist("פסיכולוג1שםפרטי", value)
    print(s)
    return {"data" : s}

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

    value = loadFiles()
    print("THIS IS THE REAL SCHDULE:")
    value[0] = list(value[0])
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
    return {"data" : value, "error" : ""}


if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)
    app.run()