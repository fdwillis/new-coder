from django.template import Context, loader
from datetime import datetime
from django.http import HttpResponse

# Create your views here.

def index(request):
	return HttpResponse("Hello, World")


def about(request):
	return HttpResponse(
		"ABOUT <a href='/'>Home</a>")

def better(request):
	t = loader.get_template('betterhello.html')
	c = Context({'current_time': datetime.now(), })
	return HttpResponse(t.render(c))