import requests

# get webpage
get = requests.get("http://www.python.org/")

# save url as html. Open in sublime as: subl test_requests.html
with open("test_requests.html", "wb") as code:
	code.write(get.content)



url = 'http://httpbin.org/post'
data = {'fname': 'Michael', 'lname': 'Herman'}

# POST requests
post = requests.post(url, data=data)

print post.content