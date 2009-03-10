# Cproject.htmlreate your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
#FORMS
from webfabric.forms import ProjectForm
from webfabric.forms import Project_ConfigurationForm
from webfabric.forms import StageForm
from webfabric.forms import TasksForm
#MODELS
from webfabric.models import Project
from webfabric.models import Project_Configuration
from webfabric.models import Template
from webfabric.models import Template_Configuration
from webfabric.models import Stage
from webfabric.models import StageTable
from webfabric.models import Tasks
from webfabric.models import Tasks_Template

#create or list a project configuration
def project_create_list(request, action='None', step=0):

#	if action == 'create':
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
			form_dict = read_form(form)
			name = form_dict['name']
			if Project.objects.filter(name=name).distinct():
				return render_to_response('project.html', {'action' : action, 'form' : form, 'error' : name})
			else: 
				description = form_dict['description']
				creation_date = form_dict['creation_date']
				creation_time = form_dict['creation_time']
				template_id = form_dict['template']
				template = Template.objects.get(id=template_id)
				p = Project(name=name, description=description, creation_date=creation_date,
				creation_time=creation_time, template=template)
				p.save()
				print 'POST project create'
				return HttpResponseRedirect('/project/create/%s' % p._get_pk_val())

		else:
			raise forms.ValidationError("form is invalid!!!") 
	else:
		if step > 0: #list projects configurations
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
			return render_to_response('project.html', {'action' : action, 
						'form' : form,
						'project_id' : step, 
						'form_configuration' : form_configuration})
		else:
			form = ProjectForm()
			
		return render_to_response('project.html', {'action' : action, 'form' : form})
		
#	else:
#		return render_to_response('project.html', {'action' : 'desconhecida'})

#saves a project configuration
def project_save(request):
	if request.method == 'POST':
		for ids in request.POST.keys():
			project_configuration = Project_Configuration.objects.get(id=ids)
			project_configuration.value = request.POST[ids]
			project_configuration.save()
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	else:
		return HttpResponse("configuration not commited")
		
#manage project stages
def project_stage(request, project_id=0, step=0):
	action = 'stage creation'
	#POST
	if request.method == 'POST':
		form = StageForm(None, request.POST)
		if form.is_valid():
			name_var = request.POST['name']
			s = Stage.objects.filter(project=project_id, name=name_var)
			p = Project.objects.filter(id=project_id)
			project_name = p[0].name
			if s:
				form = StageForm(project_id)
				return render_to_response('stage.html', {'action' : action, 
							'form' : form, 
							'error' : name_var, 
							'project' : project_name, 
							'project_id' : project_id})
			else:
				user_var = request.POST['user']
				hosts_var = request.POST['hosts']
				deploy_to_var = request.POST['deploy_to']
				p = Project.objects.get(id=project_id)
				stage = Stage(name = name_var,
						user = user_var,
						hosts = hosts_var,
						deploy_to = deploy_to_var,
						project = p)
				stage.save()
				stage = Stage.objects.filter(project=project_id)
				stage_table = StageTable(stage)
				form = StageForm(None,initial={'name' : name_var,
								'user' : user_var,
								'hosts' : hosts_var,
								'deploy_to' : deploy_to_var})
				return render_to_response('stage.html', {'action' : action, 
							'form' : form, 
							'project_name' : project_name,
							'stage' : name_var, 
							'project' : project_name, 
							'project_id' : project_id,
							'stage_table' : stage_table})
		else:
			return HttpResponse("form is not valid")
	#GET
	else:
		if step > 0:
			project = Project.objects.filter(project=project_id).values_list()
		else:
			stage = Stage.objects.filter(project=project_id)
			if stage:
				#return HttpResponse("list stages")
				stage_table = StageTable(stage)
				form = StageForm(project_id)
				p = Project.objects.filter(id=project_id)
				project_name = p[0].name
				return render_to_response('stage.html', {'action' : action, 
							'form' : form, 
							'project' : project_name,
							'project_id' : project_id,
							'stage_table' : stage_table})
			else:
				p = Project.objects.filter(id=project_id)
				if p:
					form = StageForm(project_id)
					project_name = p[0].name
					return render_to_response('stage.html', {'action' : action, 
								'form' : form, 
								'project' : project_name,
								'project_id' : project_id})
				else:
					return HttpResponse('<h2>Project does not exists</h2>')

			
#manage project tasks
def project_tasks(request, project_id=0, step=0):
	action = 'tasks creation'
	#POST
	if request.method == 'POST':
		pass
	#GET
	else:
		stage = Stage.objects.filter(project=project_id)
		if stage:
			p = Project.objects.filter(id=project_id)
			if p:
				t = Tasks.objects.filter(project=project_id)
				if t:
					tasks = Tasks.objects.filter(project=project_id)
					form = TasksForm(tasks)
					return render_to_response('tasks.html', {'action' : action, 
								'form' : form, 
								'project_id' : project_id,
								'project' : p[0].name})
				else:
					t_template = Tasks_Template.objects.filter(template=p[0].template_id)
					p_configuration = Project_Configuration.objects.filter(project=project_id)
					#TODO: Create a method to return this kind of dict mapping name to value pair from database tables
					p_dict = {}
					for x in xrange(len(p_configuration)):
						p_dict[p_configuration[x].name] = p_configuration[x].value
					print p_dict
					#saves tasks templates in the database for the respective project
					task_template_dir = settings.TASKS_TEMPLATE_DIR
					for x in xrange(len(t_template)):
						id = t_template[x].id
						name = t_template[x].name
						description = t_template[x].description
						file_ = t_template[x].file
						template_file = task_template_dir + '/' + file_
						print 'reading template file: %s' % template_file
						f_template = None
						body = None
						try:
							f_template = open(template_file, 'r')
							body = f_template.read()
							print 'done'
						finally:
							f_template.close()
						#replace variables if header file
						if name == 'header':
							body = render_to_string('tasks/' + file_, { 'application_name' : p_dict['config.application'],
									'default_tag' : p_dict['default_tag'],
									'default_clone' : p_dict['default_clone'],
									'deploy_to' : p_dict['config.deploy_to'],
									'appdjango' : p_dict['config.appdjango'],
									'releases_to_keep' : p_dict['config.releases_days_to_keep']})
						#saves template data in database
						project = Project.objects.get(id=project_id)
						t_new = Tasks(name=name, description=description, body=body,project=project)
						t_new.save()
					return HttpResponseRedirect(request.META['HTTP_REFERER'])
			else:
				return HttpResponse("<h1>Project does not exists!</h1>")
		else:
			return HttpResponse("<h1>You must create a stage before</h1>")
			

#saves a project configuration
def project_tasks_save(request, project_id=0):
	if request.method == 'POST':
		#get the number os tasks
		tasks = Tasks.objects.filter(project=project_id)
		for id in xrange(len(tasks)):
			id_aux = id + 1
			#TODO: check if the 3 keys exists, if not update just that register
			name = request.POST['name_'+str(id_aux)]
			description = request.POST['description_'+str(id_aux)]
			body = request.POST['body_'+str(id_aux)]
			task_configuration = Tasks.objects.get(id=id_aux)
			task_configuration.name = name
			task_configuration.description = description
			task_configuration.body = body
			task_configuration.save()
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	else:
		return HttpResponse("configuration not commited")
		
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
