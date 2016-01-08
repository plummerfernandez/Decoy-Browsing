"""
DECOY AMAZON BROWSING

Ammend the settings.cfg file to enter your Amazon account email and password
and prefered Amazon domain extension (.com, .co.uk, etc). Also enable wishlist on/off.

Copyright (C) 2015,  Matthew Plummer-Fernandez 
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
<http://www.gnu.org/licenses/>
#

"""

print """	
           _
    ______(.)=
   / __ \___) _________  __  __
  / / / / _ \/ ___/ __ \/ / / /_
 / /_/ /  __/ /__/ /_/ / /_/ /
/_____/\___/\___/\____/\__, /     _
    ___               /____/   __(.)=
   /   |  ____ ___  ____ _____ \___)  ____ 
  / /| | / __ `__ \/ __ `/_  / / __ \/ __ \_
 / ___ |/ / / / / / /_/ / / /_/ /_/ / / / /
/_/  |_/_/ /_/ /_/\__,_/ /___/\____/_/ /_/ 
    ____      __(.)=
   / __ )_____\___)_      _______(_)___   __
  / __  / ___/ __ \ | /| / / ___/ / __ \ /_/
 / /_/ / /  / /_/ / |/ |/ (__  ) / / / / 
/_____/_/   \____/|__/|__/____/_/_/ /_/ 



by Matthew Plummer-Fernandez, 2015 

"""

import time, random, ConfigParser
from selenium import webdriver
from random_words import RandomWords
from bs4 import BeautifulSoup

def randWord():
	rw = RandomWords()
	word = rw.random_word()
	return word


def getSigninLink(page):
	links = []
	url = ''
	for link in page.find_all('a'):
		role = link.get('data-nav-role')
		if role:
			if role == "signin":
				url = link.get('href')
				print url
	return url


def getProductLinks(domain,page):
	links = []
	for link in page.find_all('a'):
		url = link.get('href')
		if url:
			if 'http://www.amazon'+domain+'/'in url:
				if '/dp/' in url:
					if '#customerReviews' in url:
						#ignore customer review links
						notinterested = 1
					else:
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



def BrowseBot(domain, browser, wishlisting):
	visited = {}
	pList = []
	count = 0
	aurl = ""
	while True:
		#sleep to make sure page loads, add random to make it act human.
		time.sleep(random.uniform(2.1,3.9))
		
		if pList: #if there are products, browse them
			productpage = pList.pop()
			try:
				browser.get(productpage)
			except:
				print "[-] could not get page"
			count += 1
			# add to wishlist
			if wishlisting == True:
				addToWishlist(browser)
			else:
				wishing = 0			
		else: #otherwise find products via a new random search
			if len(aurl)>0:
				browser.get(aurl)

			print "[+] doing new product search"
			word = randWord()
			searchElement = browser.find_element_by_id("twotabsearchtextbox")
			time.sleep(random.uniform(0.5,1.4))
			searchElement.clear()

			searchWord = list(word)
			for i in searchWord:
				searchElement.send_keys(i)
				time.sleep(random.uniform(0.5,1.4))
			time.sleep(random.uniform(0.5,1.4))


			aurl = "http://amazon"+domain+"/s/?url=search-alias%3Daps&field-keywords="+word
			print aurl
			browser.get(aurl)
			page = BeautifulSoup(browser.page_source)
			products = getProductLinks(domain,page)
			if products:
				for productpage in products:
					if productpage not in visited:
						pList.append(productpage)
						visited[productpage] = 1
				print "before = " + str(len(pList))	
				random.shuffle(pList)
				pList = list(set(pList))[:4]
				print "after = " + str(len(pList))
		#Output 		
		print "[+] "+(browser.title).encode('ascii','ignore')+" browsed ^_^ \n("\
			+str(count)+"/"+str(len(pList))+") Visited/Queue)"
					

def Main():
	config = ConfigParser.ConfigParser()
	try:
		config.read('settings.cfg')
		print "[+] Read settings"
	except:
		print "[-] Could not read settings"

	configDomain = config.get('amazon','domain')
	configEmail = config.get('amazon','email')
	configPass = config.get('amazon','psswrd')
	configWish = config.getboolean('amazon','wishlist')

	## Initiate browser
	browser = webdriver.Firefox()
	browser.set_window_size(980,1820)
	browser.set_window_position(200,200)
	aurl = 'http://www.amazon'+configDomain
	browser.get(aurl)
	page = BeautifulSoup(browser.page_source)
	signinUrl = getSigninLink(page)
	time.sleep(random.uniform(0.5,1.4))
	browser.get(signinUrl)

	emailElement = browser.find_element_by_id("ap_email")
	configEmail2 = list(configEmail)
	for i in configEmail2:
		emailElement.send_keys(i)
		time.sleep(random.uniform(0,0.1))

	time.sleep(random.uniform(0.5,1.4))
	passElement = browser.find_element_by_id("ap_password")
	configEmail2 = list(configPass)
	for i in configEmail2:
		passElement.send_keys(i)
		time.sleep(random.uniform(0,0.1))
	time.sleep(random.uniform(0.5,1.4))
	passElement.submit()

	print "[+] Logged in to Amazon. Commencing decoy browsin'"
	
	domain = configDomain
	wishlisting = configWish
	
	BrowseBot(domain, browser, wishlisting)
	browser.close()

if __name__ == '__main__':
	Main()



