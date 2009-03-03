# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response


def project(request, action):
	if action:
		return render_to_response('project_create.html', {'action' : action})
	else:
		return HttpResponse("nenhuma action")
