#Author
#Fernando Estrada Sandoval 

from pymongo import MongoClient
import pymongo
from suds.client import Client
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import requests
import time
import sys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


def update():
	while True:
		try:
			client = MongoClient()
			db = client.Twitter_Xml
			for post in  db.coca.find({"sent":None},no_cursor_timeout=True):
				id = post['id']
				text = post['text'].replace('"',"'")
				text = text.replace("'",'').replace('%','').replace('\n','').replace('#','')
				print(text)
				sent = bot(unicode(text.encode('ascii', 'ignore')))
				print(sent)
				db.coca.update({'id':id},{'$set':{'sent':sent}},no_cursor_timeout=True)
		except pymongo.errors.OperationFailure:
			continue		

def bot(text):
	url = "https://store.apicultur.com/apis/info?name=stmtlk&version=1.0.0&provider=stmtlk"
	browser = webdriver.Chrome(executable_path=r"/home/fer/Descargas/Chrome/chromedriver")
	try:
		browser.get(url)
		timeout = 80
		sleep(5)
		i = browser.find_element_by_class_name('body-textarea')
		i.send_keys('{"texto":"'+text+'"}')
		browser.find_element_by_class_name('submit').click()

		#element_present = EC.presence_of_element_located((By.CLASS_NAME, 'block response_body'))
		#WebDriverWait(browser, timeout).until(element_present)
		sleep(80)
		html_source = browser.page_source
		
		sent=scraping(html_source)
		sleep(1)
		browser.quit()
		return sent
	except TimeoutException:
		print "TIMEOUT"#"Skipping proxy. Error occured"
		browser.quit()
    
def scraping(html):
	
	html =BeautifulSoup(html,"lxml")
	entradas = html.find('div',{'class':'block response_body'})
	aux = entradas.find('pre')
	aux = str(aux)
	x = aux[5:len(aux)-6] 
	sentimiento = x.split('<br/>')
	return sentimiento[3][18:-2]





if __name__== '__main__':
	update()