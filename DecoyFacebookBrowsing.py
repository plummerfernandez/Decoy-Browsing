"""
DECOY FACEBOOK BROWSING

Ammend the settings.cfg file to enter your Facebook account email and password.

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
/_____/\___/\___/\____/\__, /     _
    ______            /____/   __(.)=       __  
   / ____/___ _________  / /_  \___) ____  / /__
  / /_  / __ `/ ___/ _ \/ __ \/ __ \/ __ \/ //_/
 / __/ / /_/ / /__/  __/ /_/ / /_/ / /_/ / ,<   
/_/    \__,_/\___/\___/_.___/\____/\____/_/|_|  
    ____      __(.)=
   / __ )_____\___)_      _______(_)___   __
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
from nltk.corpus import names
from random import randrange

def randWord():
	rw = RandomWords()
	word = rw.random_word()
	return word


def getFacebookLinks( word, browser):
	browser.get("https://www.facebook.com/search/str/"+word+"/keywords_users")
	links = []

	time.sleep(random.uniform(2.5,3.1))

	page = BeautifulSoup(browser.page_source)
	for aTag in page.find_all('a'):
		Aclass = aTag.get('class')
		# print "class is : "+str(Aclass)
		if Aclass == ['_8o', '_8s', 'lfloat', '_ohe']:
			#for link in aTag.find_all('a'):
			url = aTag.get('href')
			if 'https://www.facebook.com' in url:
				links.append(url)
	print "[+] I found "+str(len(links))+" interesting people called "+str(word)+"! Let's loook at some!"
	return links

def getFacebookLinksPhotos(word, browser):
	browser.get("https://www.facebook.com/search/str/"+word+"/keywords_photos")
	links = []
	time.sleep(random.uniform(2.5,3.1))

	page = BeautifulSoup(browser.page_source)
	for aTag in page.find_all('a'):
		Aclass = aTag.get('class')
		# print "class is : "+str(Aclass)
		if Aclass == ['_23q']:
			#for link in aTag.find_all('a'):
			url = aTag.get('href')
			# print "LINK found ! :D : "+str(url)
			if 'https://www.facebook.com' in url:
				links.append(url)

	if links == []:
		print "[-] Couldn't find any photos that we are allowed to see"
	else:
		print "[+] Found some good photos, let's check them out!"
	return links



def createName():
	mynames = ([(name, 'male') for name in names.words('male.txt')] +
			[(name, 'female') for name in names.words('female.txt')])
	random.shuffle(mynames)
	firstname = str(mynames[0][0]).replace(' ','')
	
	return firstname

def searchFirstName(browser, word):
	searchElement = browser.find_element_by_name('q')
	searchElement.clear()
	print "[+] I searched for the name:  "+word	
	searchElement.send_keys(word)
	time.sleep(random.uniform(2,2.1))
	print "[+] I managed to type in the name "+word+"!"	
	
	return True
	
		
				
def BrowseBot(browser):
	visited = {}
	pList = []
	count = 0
	stage = 0
	while True:
		#sleep to make sure page loads, add random to make it act human.
		time.sleep(random.uniform(2.1,3.9))
		
	
		word = createName()

		if stage == 0:
			print "Stage 0 reached! "	

			result = None
			while result is None:
				try:
					result = searchFirstName(browser, word)
					if result == True:
						break
				except:
					print "[-] Had to reload Facebook :("
					browser.get("https://www.facebook.com/")
	
			page = BeautifulSoup(browser.page_source)

			print "[+] I am outside the while loop"

			
			stage+=1

		if stage == 1:
			
			print "Stage 1 reached! "
			
			if pList: #if there are products, browse them
				count+=1
				profilepage = pList.pop()
				try:
					browser.get(profilepage)
				except:
					print "[-] could not get page"
				if not pList:
					print "[-] In Plist which is now empty"
					stage = 0
			else:
				
				
				if (randrange(0,10) > 5):
					print "[+] Will search for some nice photos now!"
					profiles = getFacebookLinksPhotos(word, browser)

				else:
					print "[+] Let's see if I cann find some interesting people called "+str(word)
					profiles = getFacebookLinks(word, browser)

				if profiles:
					for profilepage in profiles:
						if profilepage not in visited:
							pList.append(profilepage)
							visited[profilepage] = 1
					print "before = " + str(len(pList))	
					random.shuffle(pList)
					pList = list(set(pList))[:4]
					print "after = " + str(len(pList))


					

def Main():
	config = ConfigParser.ConfigParser()
	try:
		config.read('settings.cfg')
		print "[+] Read settings"
	except:
		print "[-] Could not read settings"

	configEmail = config.get('facebook','email')
	configPass = config.get('facebook','psswrd')

	## Initiate browser
	browser = webdriver.Firefox()
	browser.set_window_size(980,1820)
	browser.set_window_position(200,200)
	aurl = 'http://www.facebook.com'
	browser.get(aurl)
	page = BeautifulSoup(browser.page_source)
	time.sleep(random.uniform(0.5,1.4))

	emailElement = browser.find_element_by_id("email")
	configEmail2 = list(configEmail)
	for i in configEmail2:
		emailElement.send_keys(i)
		time.sleep(random.uniform(0,0.1))

	time.sleep(random.uniform(0.5,1.4))
	passElement = browser.find_element_by_id("pass")
	configPass2 = list(configPass)
	for i in configPass2:
		passElement.send_keys(i)
		time.sleep(random.uniform(0,0.1))

	time.sleep(random.uniform(0.5,1.4))
	passElement.submit()

	print "[+] Logged in to Facebook. Commencing decoy browsin'"
	
	BrowseBot(browser)
	browser.close()

if __name__ == '__main__':
	Main()



