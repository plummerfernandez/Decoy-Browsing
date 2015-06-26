"""
DECOY GOOGLE BROWSING

Ammend the settings.cfg file to enter your Google account email and password

Copyright (C) 2015,  Matthew Plummer-Fernandez 
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
<http://www.gnu.org/licenses/>

"""

print """	
           _
    ______(.)=
   / __ \___) _________  __  __
  / / / / _ \/ ___/ __ \/ / / /_
 / /_/ /  __/ /__/ /_/ / /_/ /
/_____/\___/\___/\____/\__, /    
   ______     __(.)=  /____/_   
  / ____/___  \___) ____ _/ /__ 
 / / __/ __ \/ __ \/ __ `/ / _ \_
/ /_/ / /_/ / /_/ / /_/ / /  __/
\____/\____/\____/\__, /_/\___/ 
    ____         /____/    (.)=
   / __ )_____ ___ _     \___)___(_)___   __
  / __  / ___/ __ \ | /| / / ___/ / __ \ /_/
 / /_/ / /  / /_/ / |/ |/ (__  ) / / / / 
/_____/_/   \____/|__/|__/____/_/_/ /_/ 



by Matthew Plummer-Fernandez, 2015 *

"""
# * with the generous assistance of Leon Eckert  


import time, random, argparse, ConfigParser
from selenium import webdriver
from random_words import RandomWords
from bs4 import BeautifulSoup

def randWord():
	rw = RandomWords()
	word = rw.random_word()
	return word

def randWord2():
	rw = RandomWords()
	word1 = rw.random_word()
	word2 = rw.random_word()
	word = word1+" "+word2
	return word


def getSigninLink(page):
	links = []
	url = ''
	for link in page.find_all('a'):
		role = link.get('id')
		if role:
			if role == "gb_70":
				url = link.get('href')
				print url
	return url


def getSearchLinks(domain,page):
	links = []
	for h3Class in page.find_all('h3'):
		print h3Class
		for link in h3Class.find_all('a'):
			print link
			url = link.get('href')
			print "URL = " + str(url)
			links.append(url)
	return links


def addToWishlist(browser):
	time.sleep(random.uniform(1,2))
	try:
		wishElement = browser.find_element_by_id("add-to-wishlist-button-submit")
		if wishElement:
			print "[+] found wishlist"
			wishElement.click()
			print "[+] made wish"
		else:
			print "[-] no wishElement"
	except:
			print "[-] no wishlist button"



def BrowseBot(domain, browser):
	visited = {}
	pList = []
	count = 0
	word = ""
	while True:
		#sleep to make sure page loads, add random to make it act human.
		time.sleep(random.uniform(2.1,3.9))
		
		if pList: #if there are products, browse them
			searchPage = pList.pop()
			try:
				browser.get(searchPage)

				
			except:
				print "[-] could not get page"
			count += 1
		else: #otherwise find pages via a new random search
			if word:
				browser.get("https://www.google.co.uk/?gws_rd=ssl#q="+word)
				searchElement = browser.find_element_by_id("lst-ib")
				time.sleep(random.uniform(0.5,1.4))
				searchElement.clear()
			print "[+] doing new product search"
			word = randWord()
			searchElement = browser.find_element_by_id("lst-ib")
			searchWord = list(word)
			for i in searchWord:
				searchElement.send_keys(i)
				time.sleep(random.uniform(0.5,1.4))
			time.sleep(random.uniform(0.5,1.4))
			searchElement.submit()
			time.sleep(random.uniform(0.5,1.4))

			
			page = BeautifulSoup(browser.page_source)
			searchLinks = getSearchLinks(domain,page)
			if searchLinks:
				for searchPage in searchLinks:
						pList.append(searchPage)

				random.shuffle(pList)
				pList = list(set(pList))[:4]

					

def Main():
	config = ConfigParser.ConfigParser()
	try:
		config.read('settings.cfg')
		print "[+] Read settings"
	except:
		print "[-] Could not read settings"

	configDomain = config.get('google','domain')
	configEmail = config.get('google','email')
	configPass = config.get('google','psswrd')

	## Initiate browser
	browser = webdriver.Firefox()
	browser.set_window_size(980,1820)
	browser.set_window_position(200,200)
	aurl = 'http://www.google'+configDomain
	browser.get(aurl)
	page = BeautifulSoup(browser.page_source)
	signinUrl = getSigninLink(page)
	time.sleep(random.uniform(0.5,1.4))
	browser.get(signinUrl)
	emailElement = browser.find_element_by_id("Email")

	
	configEmail2 = list(configEmail)
	for i in configEmail2:
		emailElement.send_keys(i)
		time.sleep(random.uniform(0,0.1))

	time.sleep(random.uniform(0.5,1.4))
	emailElement.submit()
	time.sleep(random.uniform(0.5,1.4))
	passElement = browser.find_element_by_id("Passwd")
	

	configPass2 = list(configPass)
	for i in configPass2:
		passElement.send_keys(i)
		time.sleep(random.uniform(0,0.1))


	time.sleep(random.uniform(0.5,1.4))
	passElement.submit()

	print "[+] Logged in to Google. Commencing decoy browsin'"
		domain = configDomain
	
	BrowseBot(domain, browser)
	browser.close()

if __name__ == '__main__':
	Main()



