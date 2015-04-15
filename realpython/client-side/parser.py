"""Parse the Cars.xml file"""

from xml.etree import ElementTree as et
import requests

#actual file parsing
doc = et.parse("cars.xml")

# show first model
for item in doc.findall('CAR'):
	print(item.find("MAKE").text + " " +
				item.find("MODEL").text + " cost " + 
				"$" + item.find("COST").text + " dollars")


# retrieve from the web
xml = requests.get("http://www.w3schools.com/xml/cd_catalog.xml")

with open("car_parse.txt", "wb") as code:
	code.write(xml.content)

another_doc = et.parse("car_parse.txt")

for item in another_doc.findall("CD"):
	print "Album: ", item.find("TITLE").text
	print "Artist: ", item.find("ARTIST").text, '\n'