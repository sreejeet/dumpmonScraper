import urllib.request
from bs4 import BeautifulSoup
from os import path
import os
import time
import sys

# Are you connected to the internet?
try:
	urllib.request.urlopen('https://google.com').getcode()
except:
	print('Network issues. Exiting.')
	exit()

round = 1

#List of word to search
try:
	with open('key.txt') as f:
		searchList = f.read().splitlines()
except FileNotFoundError:
	print('Key file not found. Exiting.')
	exit()
#Delay for multiple rounds
delaySeconds = 0

try:
	#Reading delay from command line argument
	delaySeconds = int(sys.argv[1])
except ValueError:
	#Invalid delay value
	print("Invalid argument\nExiting...")
	exit()
except IndexError:
	#No delay argument, only one round performed
	pass

if(delaySeconds != 0):
	print("Delay set to " + str(delaySeconds) + " seconds.")

tmp = ""
while True:
	errorCount = 0
	start_time = str(time.ctime())
	log_time = time.localtime()

	#Creating logging directories
	try:
		if not os.path.exists("./logs/" + str(log_time.tm_year) +\
			"/" + str(log_time.tm_mon) + "/"):
			
			os.makedirs("./logs/" + str(log_time.tm_year) + "/" +\
				str(log_time.tm_mon) + "/")
			os.makedirs("./files/" + str(log_time.tm_year) + "/" +\
				str(log_time.tm_mon) + "/")

	except OSError as err:
		print(str(err) + "Critical Error: creating log directory")
		exit()

	log = open("./logs/" + str(log_time.tm_year) + "/" +\
		str(log_time.tm_mon) + "/" + "dumpmon_log " +\
		start_time.replace(':', '.') + ".txt", 'w')

	log.write(tmp + "Log of round " +\
		str(round) + " starting " + start_time)

	print("\n----------\nBeginning scraping round " +\
		str(round) + " on " + start_time + "...\n")

	#Retrieving last 20 tweeted dumpmon links
	page = urllib.request.urlopen("https://twitter.com/dumpmon")
	soup = BeautifulSoup(page, "html.parser")
	links = soup.find_all("span", attrs={"class":"js-display-url"})

	for link in links:

		link = link.text.replace("dumpmon", "http://www.pastebin")

		#Skipping what's already retrieved
		if(path.exists("./files/" + str(log_time.tm_year) + "/" +\
				str(log_time.tm_mon) + "/" + link[-9:-1] + ".txt")):
			#log.write(": Already retrieved")
			print("[Already retrieved] " + link)
			continue

		log.write("\n>>>" + link)
		print("[Retrieving] " + link)

		try:
			#Requesting file
			response = urllib.request.urlopen(link)
			rsp = response.read()
			rsp = str(rsp.decode("utf-8", "backslashreplace"))

			#Saving file locally
			out = open("./files/" + str(log_time.tm_year) + "/" +\
				str(log_time.tm_mon) + "/" + link[-9:-1] + ".txt",\
				'w', encoding="utf-8")
			out.write(rsp)
			out.close()
			log.write(": Retrieved")
			print("[Retrieved] " + link)


			#Searching and logging keywords
			pos = -1
			for key in searchList:
				cnt = 0
				while(True):
					pos = rsp.lower().find(key, pos+1)
					if(pos == -1):
						break
					else:
						try:
							cnt += 1
							log.write("\nFound \"" + key +\
								"\"\n-----Start snippet-----\n" +\
								rsp[pos-50:pos+50] +\
								"\n------End snippet------\n\n")
						except UnicodeEncodeError as err:
							print("[Recording error] " + str(err) + " for " + key)
							log.write("\nRecording error " + str(err) + " for " + key)
				if(cnt):
					print("[Found \"" + key + "\" X " + str(cnt) + "]")

		except urllib.error.HTTPError as err:
			log.write(": " + str(err))
			print(str(err))
			errorCount+=1

		except urllib.error.TimeoutError as err:
			log.write(": " + str(err))
			print(str(err))
			errorCount+=1

		except urllib.error.URLError as err:
			log.write(": " + str(err))
			print(str(err))
			errorCount+=1

		except socket.gaierror as err:
			log.write(": " + str(err))
			print(str(err))
			errorCount+=1
	
	#Ending round
	end_time = str(time.ctime())

	log.write("\nEnding log of round " +\
		str(round) + " on " + end_time +\
		"\n" + str(errorCount) + " error(s) occurred.")
	log.close()

	print("\nEnding scraping round " + str(round) + " on " +\
		end_time + "\n" + str(errorCount) +\
		" errors.")

	#Ending scraping
	if(delaySeconds == 0):
		break

	print("\nNext run with " +\
		str(delaySeconds) + " second(s) delay...")

	tmp = "\n\n"
	round+=1
	time.sleep(delaySeconds)
