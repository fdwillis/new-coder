import requests
import time

i = 0

# grab price once every 3 seconds for next 6 seconds

while (i < 2):
	print "test"
	base_url = "http://download.finance.yahoo.com/d/quotes.csv"

	#get data from web server
	data = requests.get(
		base_url,
		params={'s': 'GOOG', 'f': 'dl1d1t1c1ohgv', 'e': '.csv'})

	# write data to csv
	with open("stocks.csv", "a") as code:
		code.write(data.content)
	i += 1

	# pause time
	time.sleep(3)
