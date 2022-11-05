from flask import Flask, redirect, url_for, render_template, request
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
from setuptools import find_packages
import database
import os, dns
import datetime

load_dotenv()
#mongodb+srv://sdpt:<password>@cluster1.2cvf8kn.mongodb.net/?retryWrites=true&w=majority

app = Flask(__name__)

try:
    cluster = MongoClient(
        database.DATABASE_URL
        #serverSelectionTimeoutMS = 1000
    )
    # cluster = MongoClient(
    #     'mongodb+srv://sdpt:Wara03170310409@cluster1.2cvf8kn.mongodb.net/?retryWrites=true&w=majority'
    #     ,connect=False,
    #     serverSelectionTimeoutMS = 1000
    # )
    db = cluster['test']
    collection = db['hendra']
    collectionPengguna = db['pengguna']
    collectionAbsen = db['absen']

    # DbRead = collectionPengguna.find({"NIM":"19410200019"}).sort("_id", pymongo.ASCENDING)
    # listDb = list(DbRead)
    # print(listDb['NIM'])
    # findNim = collectionPengguna.find({"NIM":"19410200019"})
    # listfindNim = list(findNim)
    # print(listfindNim)
    # for data in listfindNim:
    #     coba = data
    # pengguna = collectionPengguna.find({'_id': ObjectId(str("6341757cfd3da584630b1d02"))}).sort("_id", pymongo.ASCENDING)
    # listPengguna = list(pengguna)
    # for x in listPengguna:
    #     dataEdit = x
    # print(dataEdit["NAMA"])
    # datetime_object = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    # print(datetime_object)
    #collectionPengguna.insert_one({"_id" : 10000})
    collection.insert_one({"_id":1000}) 
except:
    print("ERROR - Cannot connect to db")
###########################################

@app.route("/")
def awal():
    return render_template('home.html')

@app.route("/input/sensor")
def data():
    data = request.args.get("data")
    # push = ({"data":data})
    # collection.insert_one(push)
    return render_template('main.html', data=data)

#===========blok pengguna===============
@app.route("/datapenggunaDami")
def datapenggunaDami():
    page = 1
    return redirect(url_for('datapenggunaUtama', paging = page))

@app.route("/datapengguna/page=<paging>")
def datapenggunaUtama(paging):
    pastikanData = collectionPengguna.find().sort("_id", pymongo.ASCENDING)
    coba = list(pastikanData)
    if(len(coba)) != 0:
        DbRead = collectionPengguna.find().sort("_id", pymongo.ASCENDING)
        pages = int(paging)
        limit = 6
        starting = DbRead
        last = starting[(pages-1)*limit]["_id"]
        page = collectionPengguna.find({"_id":{'$gte':last}}).sort("_id", pymongo.ASCENDING).limit(int(limit))

        listPage = list(page)
        DbRead = list(DbRead)
        alldata = int(len(DbRead))
        
        if (alldata % limit) != 0: #jika ada sisa ketika jumlah semua data di bagi dengan limit
            jumlahPages = ((alldata//limit)+1) #berapa kali jumlah semua data dapat di bagi dengan limit dan ditambah satu untuk menentukan jumlah page website
        else:
            jumlahPages = alldata / limit
            
        
        return render_template("datapengguna.html", listPage = listPage, listUser = DbRead, pages = pages, totalPages = int(jumlahPages))
    else :
        return render_template("empty.html")

@app.route("/add_pengguna", methods=["POST", "GET"])
def add_pengguna():
    if request.method == "POST":
        try:
            nama = request.form["nama"].upper()
            nim = request.form["nim"].upper()
            prodi = request.form["prodi"].upper()
            user_baru = {"NAMA":nama, "NIM":nim, "PRODI":prodi}
            DbResponse = collectionPengguna.insert_one(user_baru)
            return redirect("/datapenggunaDami")
        except Exception as ex:
            print(ex)
    else:
        pass

@app.route("/editpengguna/<id>/page=<paging>", methods=["POST", "GET"])
def edit(id, paging):
    
    # =============menampilkan semua objek===============
    pastikanData = collectionPengguna.find().sort("_id", pymongo.ASCENDING)
    coba = list(pastikanData)
    if(len(coba)) != 0:
        DbRead = collectionPengguna.find().sort("_id", pymongo.ASCENDING)
        pages = int(paging)
        limit = 6
        starting = DbRead
        last = starting[(pages-1)*limit]["_id"]
        page = collectionPengguna.find({"_id":{'$gte':last}}).sort("_id", pymongo.ASCENDING).limit(int(limit))

        listPage = list(page)
        DbRead = list(DbRead)
        alldata = int(len(DbRead))
        
        if (alldata % limit) != 0: #jika ada sisa ketika jumlah semua data di bagi dengan limit
            jumlahPages = ((alldata//limit)+1) #berapa kali jumlah semua data dapat di bagi dengan limit dan ditambah satu untuk menentukan jumlah page website
        else:
            jumlahPages = alldata / limit
        # =============menampilkan semua objek===============
        pengguna = collectionPengguna.find({'_id': ObjectId(str(id))}).sort("_id", pymongo.ASCENDING)
        listPengguna = list(pengguna)
        for x in listPengguna:
            dataEdit = x
        return render_template("editPengguna.html", data = dataEdit, listPage = listPage, listUser = DbRead, pages = pages, totalPages = int(jumlahPages))    
    else :
        return render_template("empty.html")

@app.route("/submit_edit/<id>", methods=["POST", "GET"])
def editpengguna(id):
    filter = {'_id' : ObjectId(str(id))}
    nama = request.form["nama"].upper()
    nim = request.form["nim"].upper()
    prodi = request.form["prodi"].upper()
    newValues = {"$set" : {
    'NAMA':nama,
    'NIM':nim,
    'PRODI':prodi
    }}
    collectionPengguna.update_one(filter, newValues)
    return redirect("/datapenggunaDami")

@app.route("/deletepengguna/<id>/page=<paging>", methods=["POST", "GET"])
def deletepengguna(id, paging):
    # =============menampilkan semua objek===============
    pastikanData = collectionPengguna.find().sort("_id", pymongo.ASCENDING)
    coba = list(pastikanData)
    if(len(coba)) != 0:
        DbRead = collectionPengguna.find().sort("_id", pymongo.ASCENDING)
        pages = int(paging)
        limit = 6
        starting = DbRead
        last = starting[(pages-1)*limit]["_id"]
        page = collectionPengguna.find({"_id":{'$gte':last}}).sort("_id", pymongo.ASCENDING).limit(int(limit))

        listPage = list(page)
        DbRead = list(DbRead)
        alldata = int(len(DbRead))
        
        if (alldata % limit) != 0: #jika ada sisa ketika jumlah semua data di bagi dengan limit
            jumlahPages = ((alldata//limit)+1) #berapa kali jumlah semua data dapat di bagi dengan limit dan ditambah satu untuk menentukan jumlah page website
        else:
            jumlahPages = alldata / limit
        # =============menampilkan semua objek===============
        pengguna = collectionPengguna.find({'_id': ObjectId(str(id))}).sort("_id", pymongo.ASCENDING)
        listPengguna = list(pengguna)
        for x in listPengguna:
            dataDelete = x
        return render_template("deletePengguna.html", data = dataDelete, listPage = listPage, listUser = DbRead, pages = pages, totalPages = int(jumlahPages))    
    else :
        return render_template("empty.html")

@app.route("/submit_delete/<id>", methods=["POST", "GET"])
def submit_delete(id):
    delete = {'_id' : ObjectId(str(id))}
    collectionPengguna.delete_one(delete)
    return redirect("/datapenggunaDami")

@app.route("/infopengguna/<id>/page=<paging>", methods=["POST", "GET"])
def infopengguna(id, paging):
    # =============menampilkan semua objek===============
    pastikanData = collectionPengguna.find().sort("_id", pymongo.ASCENDING)
    coba = list(pastikanData)
    if(len(coba)) != 0:
        DbRead = collectionPengguna.find().sort("_id", pymongo.ASCENDING)
        pages = int(paging)
        limit = 6
        starting = DbRead
        last = starting[(pages-1)*limit]["_id"]
        page = collectionPengguna.find({"_id":{'$gte':last}}).sort("_id", pymongo.ASCENDING).limit(int(limit))

        listPage = list(page)
        DbRead = list(DbRead)
        alldata = int(len(DbRead))
        
        if (alldata % limit) != 0: #jika ada sisa ketika jumlah semua data di bagi dengan limit
            jumlahPages = ((alldata//limit)+1) #berapa kali jumlah semua data dapat di bagi dengan limit dan ditambah satu untuk menentukan jumlah page website
        else:
            jumlahPages = alldata / limit
        # =============menampilkan semua objek===============
        pengguna = collectionPengguna.find({'_id': ObjectId(str(id))}).sort("_id", pymongo.ASCENDING)
        listPengguna = list(pengguna)
        for x in listPengguna:
            dataInfo = x
        return render_template("infoPengguna.html", data = dataInfo, listPage = coba, listUser = DbRead, pages = pages, totalPages = int(jumlahPages))    
    else :
        return render_template("empty.html")
#===========blok pengguna===============

#===========blok Device=================
@app.route("/datadeviceDami")
def datadeviceDami():  
    page = 1
    return redirect(url_for('datadeviceUtama', paging = page))

@app.route("/datadevice/page=<paging>")
def datadeviceUtama(paging):
    pastikanData = collection.find().sort("_id", pymongo.ASCENDING)
    coba = list(pastikanData)
    if(len(coba)) != 0:
        DbRead = collection.find().sort("_id", pymongo.ASCENDING)
        pages = int(paging)
        limit = 5
        starting = DbRead
        last = starting[(pages-1)*limit]["_id"]
        page = collection.find({"_id":{'$gte':last}}).sort("_id", pymongo.ASCENDING).limit(int(limit))

        listPage = list(page)
        DbRead = list(DbRead)
        alldata = int(len(DbRead))
        
        if (alldata % limit) != 0: #jika ada sisa ketika jumlah semua data di bagi dengan limit
            jumlahPages = ((alldata//limit)+1) #berapa kali jumlah semua data dapat di bagi dengan limit dan ditambah satu untuk menentukan jumlah page website
        else:
            jumlahPages = alldata / limit
        
        return render_template("datadevice.html", listPage = listPage, listUser = DbRead, pages = pages, totalPages = int(jumlahPages))
    else:
        return render_template("deviceEmpty.html")

@app.route("/editdevice/<id>/page=<paging>")
def editDevice(id, paging):
    DbRead = collection.find().sort("_id", pymongo.ASCENDING)
    pages = int(paging)
    limit = 5
    starting = DbRead
    last = starting[(pages-1)*limit]["_id"]
    page = collection.find({"_id":{'$gte':last}}).sort("_id",pymongo.ASCENDING).limit(int(limit))
    listPage = list(page)
    DbRead = list(DbRead)
    alldata = int(len(DbRead))
    if(alldata%limit) !=0:
        jumlahPages = ((alldata//limit)+1)
    else:
        jumlahPages = alldata / limit
    pengguna = collection.find({'_id' : ObjectId(str(id))}).sort("_id", pymongo.ASCENDING)
    listPengguna = list(pengguna)
    for x in listPengguna:
        dataEdit = x
    return render_template("editDevice.html", data = dataEdit, listPage = listPage, listUser = DbRead, pages = pages, totalPages = int(jumlahPages))

@app.route("/submit_editd/<id>", methods=["POST", "GET"])
def editpenggunad(id):
    filter = {'_id' : ObjectId(str(id))}
    hastag = request.form["hastag"]
    id = request.form["id"]
    newValues = {"$set" : {
    'HASTAG':hastag,
    'ID':id
    }}
    collection.update_one(filter, newValues)
    return redirect("/datadeviceDami")

@app.route("/deletedevice/<id>/page=<paging>", methods=["POST", "GET"])
def deletedevice(id, paging):
    DbRead = collection.find().sort("_id", pymongo.ASCENDING)
    pages = int(paging)
    limit = 5
    starting = DbRead
    last = starting[(pages-1)*limit]["_id"]
    page = collection.find({"_id":{'$gte':last}}).sort("_id",pymongo.ASCENDING).limit(int(limit))
    listPage = list(page)
    DbRead = list(DbRead)
    alldata = int(len(DbRead))
    if(alldata%limit) !=0:
        jumlahPages = ((alldata//limit)+1)
    else:
        jumlahPages = alldata / limit
    pengguna = collection.find({'_id' : ObjectId(str(id))}).sort("_id", pymongo.ASCENDING)
    listPengguna = list(pengguna)
    for x in listPengguna:
        dataEdit = x
    return render_template("deleteDevice.html", data = dataEdit, listPage = listPage, listUser = DbRead, pages = pages, totalPages = int(jumlahPages))


@app.route("/submit_deleted/<id>", methods=["POST", "GET"])
def submit_deleted(id):
    delete = {'_id' : ObjectId(str(id))}
    collection.delete_one(delete)
    return redirect("/datadeviceDami")
#===========blok Device End=================

@app.route("/absen", methods=["POST", "GET"])
def absen():
    kondisi = request.args.get('kondisi')
    if kondisi == "true":
        return render_template("absen.html")
    else:
        return render_template("absenDataNotFound.html")

    
@app.route("/add_user", methods=["POST", "GET"])
def add_user():
    if request.method == "POST":
        try:
            Hastag = request.form["hastag"].upper()
            ID = request.form["ID"].upper()
            user_baru = {"HASTAG":Hastag, "ID":ID, "STATUSDEVICE":"NOT ALLOCATED"}
            DbResponse = collection.insert_one(user_baru)
            return redirect("/datadeviceDami")
        except Exception as ex:
            print(ex)
    else:
        pass


@app.route("/addabsen", methods=["POST", "GET"])
def addabsen():
    try:
        nim = request.form["nim"]
        hastag = request.form["hastag"]
        findNim = collectionPengguna.find({"NIM":nim})
        findHastag = collection.find({"HASTAG":hastag})
        for dataNim in list(findNim):
            listNim = dataNim
        for dataHastag in list(findHastag):
            listHastag = dataHastag
        dataBaru = {
                    "NAMA":listNim["NAMA"], "NIM":listNim["NIM"], "PRODI":listNim["PRODI"],
                    "HASTAG":listHastag["HASTAG"], "ID":listHastag["ID"]
                    }
        collectionAbsen.insert_one(dataBaru)
        filter = {'_id' : ObjectId(str(listHastag["_id"]))}
        collection.update_one(filter, {"$set" : {'STATUSDEVICE' : "ALLOCATED"}})
        return redirect("/absen?kondisi=true")
    except:
        return redirect("/absen?kondisi=false")
    
@app.route("/history/<id>", methods=["POST", "GET"])
def history(id):
    return render_template("report.html")

@app.route("/report")
def report():
    return render_template("report.html")

@app.route("/search/<kata>", methods=["POST", "GET"])
def search(kata):
    nim = request.form["search"]
    paging = 1
    return redirect(url_for('src', paging = paging, src = nim, kata=kata))

@app.route("/search=<src>/<kata>/page=<paging>", methods=["POST", "GET"])
def src(src, paging, kata):
    if kata == "pengguna":
        DbRead = collectionPengguna.find({"NIM":src}).sort("_id", pymongo.ASCENDING) #jumlah data yang ditemukan sesuai search dengan key hastag
        pages = int(paging)
        
        limit = 5 #jumlah device limit yang ditampilkan di page
        try: #mencoba sekaligus cek apakah data yang di cari itu ada di database
            starting = DbRead
            last = starting[(pages-1)*limit]["_id"]
        except: #jika kosong maka akan menampilkan searchEmpty.html
            return render_template("penggunasearchEmpty.html", src=src, pages=pages)
        page = collectionPengguna.find({'$and': [{"NIM":src}, {"_id":{'$gte':last}}]}).sort("NIM", pymongo.ASCENDING).limit(int(limit))

        listPage = list(page)
        DbRead = list(DbRead)
        alldata = int(len(DbRead)) 

        if (alldata % limit) != 0:
            jumlahPages = ((alldata//limit)+1)
        else:
            jumlahPages = alldata / limit

        return render_template("search.html", listPage = listPage, listUser = DbRead, pages = pages, totalPages = int(jumlahPages), src = src)

    elif kata == "device":
        DbRead = collection.find({"HASTAG":src}).sort("_id", pymongo.ASCENDING) #jumlah data yang ditemukan sesuai search dengan key hastag
        pages = int(paging)
        
        limit = 5 #jumlah device limit yang ditampilkan di page
        try: #mencoba sekaligus cek apakah data yang di cari itu ada di database
            starting = DbRead
            last = starting[(pages-1)*limit]["_id"]
        except: #jika kosong maka akan menampilkan searchEmpty.html
            return render_template("devicesearchEmpty.html", src=src, pages=pages)
        page = collection.find({'$and': [{"HASTAG":src}, {"_id":{'$gte':last}}]}).sort("HASTAG", pymongo.ASCENDING).limit(int(limit))

        listPage = list(page)
        DbRead = list(DbRead)
        alldata = int(len(DbRead)) 

        if (alldata % limit) != 0:
            jumlahPages = ((alldata//limit)+1)
        else:
            jumlahPages = alldata / limit

        return render_template("searchDevice.html", listPage = listPage, listUser = DbRead, pages = pages, totalPages = int(jumlahPages), src = src)


@app.route("/srcinfopengguna/<id>/page=<paging>", methods=["POST", "GET"])
def srcinfo(id, paging):
    DbRead = collectionPengguna.find({'_id': ObjectId(str(id))}).sort("_id", pymongo.ASCENDING)
    listDbRead = list(DbRead)
    for x in listDbRead:
        data = x
    tampilan = collectionPengguna.find({'NIM':data['NIM']}).sort("_id", pymongo.ASCENDING)

    pages = int(paging)
    limit = 5
    starting = tampilan
    last = starting[(pages-1)*limit]["_id"]
    page = collectionPengguna.find({'$and': [{"NIM":data['NIM']}, {"_id":{'$gte':last}}]}).sort("NIM", pymongo.ASCENDING).limit(int(limit))
    listPage = list(page)
    allData = int(len(listDbRead))
    if(allData % limit) != 0:
        jumlahPages = ((allData//limit)+1)
    else:
        jumlahPages = allData/limit
    
    return render_template("infoPengguna.html", data = data, listPage = listPage, listUser = listDbRead, pages = pages, totalPages = int(jumlahPages))

@app.route("/srceditpengguna/<id>/page=<paging>", methods=["POST", "GET"])
def srcedit(id, paging):
    DbRead = collectionPengguna.find({'_id': ObjectId(str(id))}).sort("_id", pymongo.ASCENDING)
    listDbRead = list(DbRead)
    for x in listDbRead:
        data = x
    tampilan = collectionPengguna.find({'NIM':data['NIM']}).sort("_id", pymongo.ASCENDING)

    pages = int(paging)
    limit = 5
    starting = tampilan
    last = starting[(pages-1)*limit]["_id"]
    page = collectionPengguna.find({'$and': [{"NIM":data['NIM']}, {"_id":{'$gte':last}}]}).sort("NIM", pymongo.ASCENDING).limit(int(limit))
    listPage = list(page)
    allData = int(len(listDbRead))
    if(allData % limit) != 0:
        jumlahPages = ((allData//limit)+1)
    else:
        jumlahPages = allData/limit
    
    return render_template("editPengguna.html", data = data, listPage = listPage, listUser = listDbRead, pages = pages, totalPages = int(jumlahPages))

@app.route("/srcdeletepengguna/<id>/page=<paging>", methods=["POST", "GET"])
def srcedelete(id, paging):
    DbRead = collectionPengguna.find({'_id': ObjectId(str(id))}).sort("_id", pymongo.ASCENDING)
    listDbRead = list(DbRead)
    for x in listDbRead:
        data = x
    tampilan = collectionPengguna.find({'NIM':data['NIM']}).sort("_id", pymongo.ASCENDING)

    pages = int(paging)
    limit = 5
    starting = tampilan
    last = starting[(pages-1)*limit]["_id"]
    page = collectionPengguna.find({'$and': [{"NIM":data['NIM']}, {"_id":{'$gte':last}}]}).sort("NIM", pymongo.ASCENDING).limit(int(limit))
    listPage = list(page)
    allData = int(len(listDbRead))
    if(allData % limit) != 0:
        jumlahPages = ((allData//limit)+1)
    else:
        jumlahPages = allData/limit
    
    return render_template("deletePengguna.html", data = data, listPage = listPage, listUser = listDbRead, pages = pages, totalPages = int(jumlahPages))


###########################################
if __name__ == "__main__":
    app.run(port=9090, debug=True,host='0.0.0.0')