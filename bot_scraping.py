#!/usr/bin/python
# -*- coding: UTF8 -*-
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import requests
import time
import sys


def bot(text):
	url = "https://store.apicultur.com/apis/info?name=stmtlk&version=1.0.0&provider=stmtlk"
	browser = webdriver.Chrome(executable_path=r"/home/fer/Descargas/Chrome/chromedriver")
	try:
		browser.get(url)
		sleep(5)
		i = browser.find_element_by_class_name('body-textarea')
		i.send_keys('{"texto":"'+text+'"}')
		
		browser.find_element_by_class_name('submit').click()
		sleep(3)
		html_source = browser.page_source
		sent=scraping(html_source)
		#sleep(30000)
		browser.quit()
		return sent
		
		  
	except Exception,e:
		print e#"Skipping proxy. Error occured"
		browser.quit()
    
def scraping(html):
	
	html =BeautifulSoup(html,"lxml")
	print(html)
	entradas = html.find('div',{'class':'block response_body'})
	aux = entradas.find('pre')
	aux = str(aux)
	x = aux[5:len(aux)-6] 
	sentimiento = x.split('<br/>')
	return sentimiento[3][18:-2]
		
if __name__ == '__main__':
	cad = "te amo más que otro días"
	s= bot(cad.decode('utf-8'))
	print(s)	
