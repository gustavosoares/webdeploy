# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render_to_response
from webfabric.forms import ProjectForm
from webfabric.models import Project
from webfabric.models import Template

def project(request, action, step):

#	if action == 'create':
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			if Project.objects.filter(name=name).distinct():
				return render_to_response('error.html', {'msg' : "O projeto %s ja existe!!!!" % name})
			else: 
				description = form.cleaned_data['description']
				creation_date = form.cleaned_data['creation_date']
				creation_time = form.cleaned_data['creation_time']
				template_id = form.cleaned_data['template']
				template = Template.objects.get(id=template_id)
				p = Project(name=name, description=description, creation_date=creation_date,
				creation_time=creation_time, template=template)
				p.save()
				return HttpResponseRedirect('/project/create/%s' % p._get_pk_val())
				#return render_to_response('project_create.html', {'action' : action, 'form' : form, 'step' : 1})
		else:
			raise forms.ValidationError("form is invalid!!!") 
	else:
		form = ProjectForm()
		return render_to_response('project_create.html', {'action' : action, 'form' : form})
		
#	else:
#		return render_to_response('project_create.html', {'action' : 'desconhecida'})
