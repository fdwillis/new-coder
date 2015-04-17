import requests
import time

i = 1

# grab price once every 5 min for the next hour

while (i <= 1):
	print i
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
	time.sleep(2)
