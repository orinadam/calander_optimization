import os
import sys
import logging
import base64 

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    return "good"
    
        



    # connect to the database

    # use the algorithm to send the schedule

    #return schedule
    return "check1"


if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)
    app.run()