# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from webfabric.forms import ProjectForm


def project(request, action):

	if action == 'create':
		
		form = ProjectForm()
		return render_to_response('project_create.html', {'action' : action, 'form' : form})
		
	else:
		return render_to_response('project_create.html', {'action' : 'desconhecida'})
