from flask import Flask, render_template, request, jsonify
import requests
from flask_mongokit import MongoKit
from mongokit import Document, Connection
import json
import threading
from time import time

class EmbedDoc(Document):
   __collection__ = 'tuits'
   structure = {
      'geometry':{
         'type':str,
         'coordinates':[],
       },
       'properties':{
          'street':unicode,
          'city':unicode,
          'day':unicode,
          'fecha':unicode,
          'hora':unicode,
          'subtype':unicode,
        }
   }
   default_values = {'geometry.type':'Point','properties.city':'desconocido'}
    
class MyDocument(Document):
    __collection__='tuits'
    structure = {
        'type':str,
        'features':[EmbedDoc],
    }
    required_fields = ['type']
    default_values = {'type':'FeatureCollection'}
    
embebed = 0
threads = list()

arr=list()
a=list()
x=list()
w={}
app = Flask(__name__)
db = MongoKit(app)
db.register([EmbedDoc,MyDocument])
lock = threading.Lock()
datos_locales = threading.local()    

		
@app.route('/')
def index():
	return render_template('flot.html')



@app.route('/mongo', methods=["POST"])
def conecta_mongo():
	app.config['MONGODB_DATABASE']='Waze'
	app.config['MONGODB_HOST']='localhost'
	
	with app.app_context():
		tiempo_inicial = time()
		#a = db.tuits.find({'$and':[{'geometry':{'$ne':None}},{'sent':{'$ne':None}}]},{'_id':0,'text':1,'sent':1,'geometry':1,'day':1})
		a= db.reportes.find({'$and':[{"subtype":{'$ne':None}},{"day":{'$ne':None}},{"type":"ACCIDENT"},{"street":{'$ne':None}},{"city":{'$ne':None}}]},{"street":1,"city":1,"fecha":1,"day":1,"location":1,"hora":1,"subtype":1,"_id":0})
		a = list(a)
		
		x=construye(a)
		#print(len(x))
		mydoc = db.MyDocument()
		mydoc['features']=x
		mydoc.save()
		w = mydoc.to_json()
		tiempo_final = time()
		tiempo_ejecucion = tiempo_final - tiempo_inicial
		print 'El tiempo de ejecucion fue:',tiempo_ejecucion
	#	print(w)#"""
		return json.dumps(w)

def construye(l):
	
	#for i in range(0,len(l)-1):
	i=0
	while True:
		if(i<=len(l)-4):
			embebed = db.EmbedDoc()
			t = threading.Thread(target=uso_hilos, args=(embebed,l[i]))
			threads.append(t)
			t.start()
		
			embebed = db.EmbedDoc()
			q = threading.Thread(target=uso_hilos, args=(embebed,l[i+1]))
			threads.append(q)
			q.start()
			
			embebed = db.EmbedDoc()
			j = threading.Thread(target=uso_hilos, args=(embebed,l[i+2]))
			threads.append(j)
			j.start()
			
			embebed = db.EmbedDoc()
			x = threading.Thread(target=uso_hilos, args=(embebed,l[i+3]))
			threads.append(x)
			x.start()
			
			q.join()	
			t.join()
			j.join()
			x.join()
			i+=4
		else:
			break
		
		#uso_hilos(embebed,post)
	return arr
		#"""
def uso_hilos(embebed,post):

	lock.acquire()
	geo=[]
	geo.append(post['location']['x'])
	geo.append(post['location']['y'])

	embebed['geometry']['coordinates']=geo
	embebed['properties']['street']=post['street']
	embebed['properties']['city']=post['city']
	embebed['properties']['fecha']=post['fecha']
	embebed['properties']['day']=post['day']
	embebed['properties']['hora']=post['hora']
	embebed['properties']['subtype']=post['subtype']
	embebed.validate()
	embebed.validation_errors
	embebed.save()
	arr.append(embebed)
	lock.release()
	
if __name__ == '__main__':
    app.run(host="127.0.0.1",
    threaded=True)
