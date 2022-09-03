from flask import Flask, redirect, url_for, render_template, request
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import database

app = Flask(__name__)

try:
    cluster = MongoClient(
        database.database
        ,connect=False,
        serverSelectionTimeoutMS = 1000
    )
    db = cluster['test']
    collection = db['test'] 
except:
    print("ERROR - Cannot connect to db")
###########################################

@app.route("/")
def awal():
    return("Selamat datang")

@app.route("/input/sensor")
def data():
    data = request.args.get("data")
    push = ({"data":data})
    collection.insert_one(push)
    return("nilai adalah {}".format(data))

###########################################
if __name__ == "__main__":
    app.run(port=9090, debug=True,host='0.0.0.0')