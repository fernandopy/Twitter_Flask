#!/usr/bin/python
# -*- coding: UTF8 -*-
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
from pymongo import MongoClient
import pymongo
import requests.packages.urllib3
from suds.client import Client
import unirest

requests.packages.urllib3.disable_warnings()


class StdOutListener(StreamListener):
    def on_data(self,data):
        #print('Tweet text: ' + data)
        js = json.loads(data)
        cord = js['coordinates']
        #print (cord)
        map(js.pop,['coordinates'])#para remover una llave
        js['geometry']=cord
        
        
        #print(js['text'].encode('utf8','replace'))
        print(js['text'])
        #print(self.sent(js['text'].encode('utf8','replace')))
        #print(self.sentimientos("eres un pendejo"))
        js['sent']=self.sentimientos(js['text'].encode('utf8','replace'))
        print(js['sent'])
        js['day']=self.ConoceDia(str(js['timestamp_ms']))
        
            
        #self.sentimientos('holá'.decode('utf8','replace'))
        #print(js['geometry'])
        
        try:
            client = MongoClient()
            db = client.Twitter_Xml#Twitter es el nombre de la base
            db.epn.insert(js)
            print "----"
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to server: %s" % e
        #print(js['entities']['hashtags'])#es una lista
        #map(js.pop,['entities'])#para remover una llave
        #js['perro'] = 'huevos'#para agregar una llave al diccionario
        #print(js['perro'])
        
    def sentimientos(self,tuit):
        requests.packages.urllib3.disable_warnings()
        sent = None
        apikey = 'ab881ef9-5941-45d7-95a7-595fc89d129d'
        lenguaje = 'spa'
        ligaPeticion ='https://api.havenondemand.com/1/api/sync/analyzesentiment/v1?text={0}&language={1}&apikey={2}'
        ligaPeticion = ligaPeticion.format(tuit,lenguaje,apikey)
        try:
            jsonRespuesta= requests.get(ligaPeticion).json()
            sent = jsonRespuesta["aggregate"]["sentiment"]
        except:
            sent = self.sent(tuit)
        return sent
    
    def sent (self,tuit):
		# These code snippets use an open-source library. http://unirest.io/python
		response = unirest.post("https://community-sentiment.p.mashape.com/text/",
			headers={"X-Mashape-Key": "XW6ZAgErxomshcOBCKM01jEP4Sbwp1ubwsAjsnIhPblvxkTJU7","Content-Type": "application/x-www-form-urlencoded","Accept": "application/json"},
			params={
				"txt": tuit#"feliz"#tuit#"Trabajando horas extras my lord @EPN  para que la gaviota use esas tangas que se le ven perfectas, lo bueno casi no cuenta...."
			}
		)
		return response.body['result']['sentiment']
		

    def ConoceDia(self,time):
        url = 'http://localhost/SaberDia/nuSoap.php?wsdl'
        client = Client(url)
        #datos={'email':'xxx@gmail.com','nombre':'fernando','telefono':'56907500','ano_nac':'28/10/1988'}
        client.options.cache.clear() #make this line
        cl=client.service.dia_tuit(time)
        return cl



 
 
    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True # To continue listening
 
    def on_timeout(self):
        print('Timeout...')
        return True # To continue listening
 
if __name__ == '__main__':
    access_token = "3253347468-48d57nPHkARxBKMKl7j9DWueevTNsdpYLykOvIM"
    access_token_secret = "Smpknn1UM7LGE1Qref9B9TRREI2poiYBWlBrUrT0oK3Tz"
    consumer_key = "B4jE08jICKyeNh7aob8fACuF2"
    consumer_secret = "DGnEKSAaWtagLESCD4QktYX9JIDjngjr7NAJ0e3erIzJg0aH4L"
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)
    stream.filter(locations=[-99.36666666,19.05,-98.95,19.6],track=['epn','EPN'])
    #stream.filter(track=['PenaNieto','EPN'])
    #stream.filter(locations=[-118.407,14.53209836,-86.71040527,32.718653],languages=['es'],track=['epn','EPN'])
	#stream.filter(locations=[-99.36666666,19.05,-98.95,19.6],track=['epn','EPN'])
	
