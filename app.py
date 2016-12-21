from flask import Flask, render_template, request, jsonify
import requests
from flask_mongokit import MongoKit
from mongokit import Document, Connection
import json
import threading
from time import time
from bson.code import Code

class EmbedDoc(Document):
	 __collection__ = 'tuits'
	 structure = {
         'geometry':{
         	'type':unicode,
         	'coordinates':[],
         },
         'properties':{
         	'text':unicode,
         	'sent':unicode,
         	'day':unicode,
         }
     }

class MyDocument(Document):
    __collection__='tuits'
    structure = {
        'type':str,
        'features':[EmbedDoc],
    }
    required_fields = ['type']
    default_values = {'type':'FeatureCollection'}
    

arr=list()
a=list()
x=list()
w={}

app = Flask(__name__)
db = MongoKit(app)

db.register([EmbedDoc,MyDocument])
lock = threading.Lock()

		
@app.route('/')
def index():
	return render_template('flot.html')



@app.route('/mongo', methods=["POST"])
def conecta_mongo():
	app.config['MONGODB_DATABASE']='Twitter_Xml'
	app.config['MONGODB_HOST']='localhost'
	
	with app.app_context():
		tiempo_inicial = time()
		a = db.tuits.find({'$and':[{'geometry':{'$ne':None}},{'sent':{'$ne':None}}]},{'_id':0,'text':1,'sent':1,'geometry':1,'day':1})
		a = list(a)
		construye(a)
		
		mydoc = db.MyDocument()
		mydoc['features']=arr
		mydoc.save()
		w = mydoc.to_json()
		tiempo_final = time()
		tiempo_ejecucion = tiempo_final - tiempo_inicial
		print 'El tiempo de ejecucion fue:',tiempo_ejecucion
		return json.dumps(w)

def construye(l):
	i=0
	while True:
		if(i<=len(l)-4):
			embebed = db.EmbedDoc()
			t = threading.Thread(target=uso_hilos, args=(embebed,l[i]))
			t.start()
		
			embebed = db.EmbedDoc()
			q = threading.Thread(target=uso_hilos, args=(embebed,l[i+1]))
			q.start()
			
			embebed = db.EmbedDoc()
			j = threading.Thread(target=uso_hilos, args=(embebed,l[i+2]))
			j.start()
			
			embebed = db.EmbedDoc()
			x = threading.Thread(target=uso_hilos, args=(embebed,l[i+3]))
			x.start()
			
			q.join()	
			t.join()
			j.join()
			x.join()
			i+=4
		else:
			break
	#return arr
		#"""
def uso_hilos(embebed,post):
	
	embebed['geometry']['type']=post['geometry']['type']
	embebed['geometry']['coordinates']=post['geometry']['coordinates']
	embebed['properties']['text']=post['text']
	embebed['properties']['sent']=post['sent']
	embebed['properties']['day']=post['day']
	embebed.validate()
	embebed.validation_errors
	embebed.save()
	lock.acquire()
	arr.append(embebed)
	lock.release()

@app.route('/grafica', methods=["POST"])
def grafica():
	label=[]
	cant=[]
	app.config['MONGODB_DATABASE']='Twitter_Xml'
	app.config['MONGODB_HOST']='localhost'

	#a = db.coca.aggregate([{'$match':{'$and':[{'text':{'$regex':'interjet','$options':'i'}},{'sent',{'$ne':'s report'}}]}},{'$group':{'_id':'$sent','suma':{'$sum':1}}}])
	a = db.coca.aggregate([{'$match':{'$and':[{'text':{'$regex':'interjet','$options':'i'}},{'sent':{'$ne':'s report'}}]}},{'$group':{'_id':'$sent','suma':{'$sum':1}}}])
	b = list(db.coca.find({'$and':[{'text':{'$regex':'interjet','$options':'i'}}]},{"text":1,"sent":1,"day":1,"_id":0}))
	print(a)
	res = a["result"]
	for i in res:
		label.append(i["_id"])
		cant.append(i["suma"])
	arr = {"label":label,"cantidad":cant,"lista":b}	
	return json.dumps(arr)
	


if __name__ == '__main__':
    app.run(host="127.0.0.1",port='8080',
    threaded=True)
