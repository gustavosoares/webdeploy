# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render_to_response
from webfabric.forms import ProjectForm
from webfabric.forms import Project_ConfigurationForm
from webfabric.models import Project
from webfabric.models import Project_Configuration
from webfabric.models import Template
from webfabric.models import Template_Configuration

def project(request, action, step=0):

#	if action == 'create':
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
			form_dict = read_form(form)
			name = form_dict['name']
			if Project.objects.filter(name=name).distinct():
				return render_to_response('project_create.html', {'action' : action, 'form' : form, 'error' : name})
			else: 
				description = form_dict['description']
				creation_date = form_dict['creation_date']
				creation_time = form_dict['creation_time']
				template_id = form_dict['template']
				template = Template.objects.get(id=template_id)
				p = Project(name=name, description=description, creation_date=creation_date,
				creation_time=creation_time, template=template)
				p.save()
				return HttpResponseRedirect('/project/create/%s' % p._get_pk_val())
				#return render_to_response('project_create.html', {'action' : action, 'form' : form, 'step' : 1})
		else:
			raise forms.ValidationError("form is invalid!!!") 
	else:
		if step > 0:
			project = Project.objects.get(id=step)
			form = ProjectForm(initial={'name' : project.name,
				'description' : project.description,
				'creation_date' : project.creation_date,
				'creation_time' : project.creation_time,
				'template' : project.template_id
				})
			#project configuration exists?
			p_configuration = Project_Configuration.objects.filter(project=step).values_list()
			if not p_configuration:
				template_configuration = Template_Configuration.objects.filter(template=project.template_id).values_list()
				for t in template_configuration:
					tupla = t
					name = tupla[1]
					value = tupla[2]
					p = Project_Configuration(name = name,
								value = value,
								project_id = step
								)
					p.save()
				p_configuration = Project_Configuration.objects.filter(project=step).values_list()
			
			form_configuration = Project_ConfigurationForm(p_configuration)
			return render_to_response('project_create.html', {'action' : action, 'form' : form, 'form_configuration' : form_configuration})
		else:
			form = ProjectForm()
			
		return render_to_response('project_create.html', {'action' : action, 'form' : form})
		
#	else:
#		return render_to_response('project_create.html', {'action' : 'desconhecida'})

#return a dict from a project form
def read_form(form):
	name = form.cleaned_data['name']
	description = form.cleaned_data['description']
	creation_date = form.cleaned_data['creation_date']
	creation_time = form.cleaned_data['creation_time']
	template_id = form.cleaned_data['template']
		
	form_dict = { 
		'name' : name, 
		'description' : description, 
		'creation_date' : creation_date,
		'creation_time' : creation_time,
		'template' : template_id
		}
	
	return form_dict
