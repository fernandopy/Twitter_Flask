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
import six
from six.moves import http_client as httplib
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import requests
import threading

requests.packages.urllib3.disable_warnings()


class StdOutListener(StreamListener):
    def on_data(self,data):
		js = json.loads(data)
		cord = js['coordinates']
		map(js.pop,['coordinates'])#para remover una llave
		js['geometry']=cord
		print(js['text'])
		#js['sent']=self.sentimientos(js['text'].encode('utf8','replace'))
		#print(js['sent'])
		print('------------------')
		js['day']=self.ConoceDia(str(js['timestamp_ms']))
		try:
			client = MongoClient()
			db = client.Twitter_Xml#Twitter es el nombre de la base
			db.coca.insert(js)
			print "----"
		except pymongo.errors.ConnectionFailure, e:
			print "Could not connect to server: %s" % e
    
    
    
    
    
    def sentimientos(self,tuit):
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
		response = unirest.post("https://community-sentiment.p.mashape.com/text/",
			headers={"X-Mashape-Key": "XW6ZAgErxomshcOBCKM01jEP4Sbwp1ubwsAjsnIhPblvxkTJU7","Content-Type": "application/x-www-form-urlencoded","Accept": "application/json"},
			params={
				"txt": tuit
			}
		)
		return response.body['result']['sentiment']#"""
		

    def ConoceDia(self,time):
        url = 'http://localhost/SaberDia/nuSoap.php?wsdl'
        client = Client(url)
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
	
	while True:
		try:
			access_token = "3253347468-48d57nPHkARxBKMKl7j9DWueevTNsdpYLykOvIM"
			access_token_secret = "Smpknn1UM7LGE1Qref9B9TRREI2poiYBWlBrUrT0oK3Tz"
			consumer_key = "B4jE08jICKyeNh7aob8fACuF2"
			consumer_secret = "DGnEKSAaWtagLESCD4QktYX9JIDjngjr7NAJ0e3erIzJg0aH4L"
			listener = StdOutListener()
			auth = OAuthHandler(consumer_key, consumer_secret)
			auth.set_access_token(access_token, access_token_secret)
			stream = Stream(auth, listener)
			#stream.filter(locations=[-118.407,14.53209836,-86.71040527,32.718653],languages=['es'],track=['cocacola','pepsi'])
			#stream.filter(locations=[-99.36666666,19.05,-98.95,19.6],track=['epn','EPN'])
			stream.filter(track=['interjet','aereomexico','volaris'])
			#stream.filter(locations=[-118.407,14.53209836,-86.71040527,32.718653],languages=['es'],track=['trafico','muertes'],stall_warnings=True)
			#stream.filter(locations=[-99.36666666,19.05,-98.95,19.6],languages=['es'],track=['epn','EPN'])
			
		except :
			continue
			print('error')
