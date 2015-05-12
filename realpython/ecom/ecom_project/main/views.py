from django.shortcuts import render_to_response
from django.template import RequestContext
from payments.models import User
import pdb

# Views

def index(request):
	uid = request.session.get('user')
	# pdb.set_trace()
	if uid is None:
		return render_to_response('main/index.html')
	else:
		return render_to_response(
			'main/user.html', 
			{'user': User.get_by_id(uid)}
		)