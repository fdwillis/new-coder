import json
import requests

url = "http://maps.googleapis.com/maps/api/directions/json?origin=Central+Park&destination=Times+Square&sensor=false&mode=walking"
data = requests.get(url)
binary = data.content
output = json.loads(binary)

print output['status']

for route in output['routes']:
	for leg in route['legs']:
		for step in leg['steps']:
			print step['html_instructions']