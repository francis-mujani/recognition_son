from flask import Flask, jsonify, request, render_template, make_response, url_for
from flask_restful import Resource, Api, reqparse
import numpy as np
import pandas as pd
import os, sys
import time

# from recognize_microphone import run
# sys.path.insert(1, '/home/dreamchasers/Documents/shazam/audio-fingerprint-identifying-python')
#os.chdir('../')
sys.path.append(os.path.realpath('.'))
from recognize_microphone import run
#from .. recognize_microphone import run
from root import CONFIG_PATH

# from libs.db_sqlite import SqliteDatabase
# from libs.config import get_config


# config = get_config()
# db = SqliteDatabase()
names = []


app = Flask(__name__)

# route 
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/fitmusic", methods=["POST"])
def getmusic():
    if request.method == "POST":
        data = run()
        return data
    return jsonify({"error":"Le son n'existe pas dans la base de donnée !"})


# create port
port = int(os.environ.get("PORT", 5001))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)

