from flask import Flask, redirect, url_for, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
import database
import os, dns

load_dotenv()
#mongodb+srv://sdpt:<password>@cluster1.2cvf8kn.mongodb.net/?retryWrites=true&w=majority

app = Flask(__name__)

try:
    cluster = MongoClient(
        database.DATABASE_URL
    )
    # cluster = MongoClient(
    #     'mongodb+srv://sdpt:Wara03170310409@cluster1.2cvf8kn.mongodb.net/?retryWrites=true&w=majority'
    #     ,connect=False,
    #     serverSelectionTimeoutMS = 1000
    # )
    db = cluster['test']
    collection = db['hendra']
    collection.insert_one({"_id":100}) 
except:
    print("ERROR - Cannot connect to db")
###########################################

@app.route("/")
def awal():
    return ('Selamat datang semuanya')

@app.route("/input/sensor")
def data():
    data = request.args.get("data")
    # push = ({"data":data})
    # collection.insert_one(push)
    return render_template('main.html', data=data)

###########################################
if __name__ == "__main__":
    app.run(port=9090, debug=True,host='0.0.0.0')