# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response


def project(request, action):
	if action:
		html = "<html><body>action %s.</body></html>" % action
		return HttpResponse(html)
	else:
		return HttpResponse("nenhuma action")