from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from .forms import ContactView
from django.contrib import messages

def contact(request):
	if request.method == "POST":
		form = ContactView(request.POST)
		if form.is_valid():
			our_form = form.save(commit = True )
			our_form.save()
			messages.add_message(
				request, messages.INFO, 'Custom Message After Form Submitted'
			)
			return HttpResponseRedirect('/')
	else:
		form = ContactView()
	t = loader.get_template('contact.html')
	c = RequestContext(request, { 'form': form, })
	return HttpResponse(t.render(c))