import urllib.request
from bs4 import BeautifulSoup
from os import path
import os
import time

# Setting timezone
os.environ['TZ'] = 'Asia/Kolkata'
time.tzset()

# Is your Internet working?
try:
	urllib.request.urlopen('http://google.com')
except Exception as err:
	print('Network connection error', err)
	exit()

round = 1
delaySeconds = 600
keyFile = "key.txt"
tmp = ""

# List of word to search
try:
	with open(keyFile) as f:
		searchList = f.read().splitlines()
	print("Using " + keyFile + " for keyword searching.")
except:
	print("No keyword file found.")
	searchList=[]

while True:
	errorCount = 0
	start_time = str(time.ctime())
	log_time = time.localtime()

	fileTime =	str(log_time.tm_year)\
	+ str(log_time.tm_mon).zfill(2)\
	+ str(log_time.tm_mday).zfill(2)\
	+ "-"\
	+ str(log_time.tm_hour).zfill(2)\
	+ str(log_time.tm_min).zfill(2)\
	+ str(log_time.tm_sec).zfill(2)

	# Creating logging directories
	try:
		if not os.path.exists("./logs/"
			+ str(log_time.tm_year)
			+ "/" + str(log_time.tm_mon) + "/"):

			os.makedirs("./logs/"
				+ str(log_time.tm_year)
				+ "/" +	str(log_time.tm_mon) + "/")

			os.makedirs("./files/"
				+ str(log_time.tm_year)
				+ "/" +	str(log_time.tm_mon) + "/")

	except OSError as err:
		print(str(err) + "Critical Error: creating log directory")
		exit()

	nothingFound = True
	logFilePath = "./logs/"\
		+ str(log_time.tm_year)\
		+ "/" + str(log_time.tm_mon)\
		+ "/" + "dumpmon_"\
		+ fileTime\
		+ ".txt"
	log = open(logFilePath, 'w')

	log.write(tmp
		+ "Log of round "
		+ str(round)
		+ " starting "
		+ start_time)

	# print("\n----------\nBeginning scraping round " +\
		# str(round) + " on " + start_time + "...\n")
	print('\n' + str(round).zfill(3) + ' ' + fileTime)

	# Retrieving last 20 tweeted dumpmon links
	page = urllib.request.urlopen("https://twitter.com/dumpmon")
	soup = BeautifulSoup(page, "html.parser")
	links = soup.find_all("span", attrs={"class":"js-display-url"})
	links.reverse()

	for link in links:

		link = link.text.replace("dumpmon", "http://www.pastebin")

		# Skipping what's already retrieved
		if(path.exists("./files/"
			+ str(log_time.tm_year)
			+ "/" +	str(log_time.tm_mon)
			+ "/" + link[-9:-1] + ".txt")):
			# log.write(": Already retrieved")
			# print("[Already retrieved] " + link)
			continue

		log.write("\n>>>" + link)
		# print("[Retrieving] " + link)

		try:
			# Requesting file
			response = urllib.request.urlopen(link)
			try:
				rsp = response.read().decode('utf-8', 'backslashreplace')
			except:
				TypeError
				log.write(": TypeError. Cannot decode file.")
				print("TypeError Cannot decode file")
				continue
				UnicodeDecodeError
				log.write(": UnicodeDecodeError. Cannot decode file.")
				print("UnicodeDecodeError. Cannot decode file.")
				continue

			# Saving file locally
			out = open("./files/"
				+ str(log_time.tm_year)
				+ "/" +	str(log_time.tm_mon)
				+ "/" + link[-9:-1] + ".txt"
				, 'w', encoding="utf-8")

			out.write(rsp)
			out.close()
			log.write(": Retrieved")
			# print("[Retrieved] " + link)

			# Searching and logging keywords
			pos = -1
			for key in searchList:
				cnt = 0
				while(True):
					pos = rsp.lower().find(key, pos+1)
					if(pos == -1):
						break
					else:
						nothingFound = False
						try:
							cnt += 1
							log.write("\nFound \""
								+ key
								+ "\"\n-----Start snippet-----\n"
								+ rsp[pos-50:pos+50]
								+ "\n------End snippet------\n")
						except UnicodeEncodeError as err:
							print("[Recording error] " + str(err) + " for " + key)
							log.write("\nRecording error " + str(err) + " for " + key)
				if(cnt):
					print("[Found \"" + key + "\" X " + str(cnt) + "]")

		except urllib.error.HTTPError as err:
			log.write(": " + str(err))
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

	# Ending round
	end_time = str(time.ctime())

	log.write("\nEnding log of round "
		+ str(round) + " on " + end_time
		+ "\n" + str(errorCount)
		+ " error(s) occurred.")
	log.close()

	# print("\nEnding scraping round " + str(round) + " on " +\
		# end_time + "\n" + str(errorCount) +\
		# " errors.")

	# print('\n--End round ' + str(round).zfill(3) + ' ' + end_time)

	# Removing log if nothing found
	if nothingFound:
		os.system('rm ' + logFilePath)

	# Ending scraping
	if(delaySeconds == 0):
		break

	# print("\nNext run with " +\
		# str(delaySeconds) + " second(s) delay...")

	tmp = "\n\n"
	round+=1
	time.sleep(delaySeconds)
