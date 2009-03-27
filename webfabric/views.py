# -*- coding: utf-8 -*-
import datetime
import os
import commands
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
from webfabric.forms import Project_ManageForm
from webfabric.forms import StageForm
from webfabric.forms import FabfileForm
#MODELS
from webfabric.models import Project
from webfabric.models import Project_Configuration
from webfabric.models import Template
from webfabric.models import Template_Configuration
from webfabric.models import Stage
from webfabric.models import StageTable
from webfabric.models import Tasks
from webfabric.models import Fabfile_Template
from webfabric.models import Fabfile

#list projects or get configuration for project_id
def project_save(request, project_id):
	
	form = ProjectForm(request.POST)
	if form.is_valid():
		form_dict = read_form(form)
		name = form_dict['name']
		if Project.objects.filter(name=name).distinct():
			return render_to_response('project.html', {'form' : form, 'error' : name})
		else: 
			description = form_dict['description']
			creation_date = form_dict['creation_date']
			creation_time = form_dict['creation_time']
			template_id = form_dict['template']
			template = Template.objects.get(id=template_id)
			p = Project(name=name, description=description, creation_date=creation_date,
			creation_time=creation_time, template=template)
			p.save()
			print 'new project created'
			return HttpResponseRedirect('/project/%s' % p._get_pk_val())

	else:
		raise forms.ValidationError("form is invalid!!!")

def project(request, project_id=0):
	#POST
	if request.method == 'POST':
		return project_save(request, project_id)
	#GET
	else:
		if project_id > 0: #list projects configurations
			project = Project.objects.get(id=project_id)
			form = ProjectForm(initial={'name' : project.name,
				'description' : project.description,
				'creation_date' : project.creation_date,
				'creation_time' : project.creation_time,
				'template' : project.template_id
				})
			#project configuration exists?
			p_configuration = Project_Configuration.objects.filter(project=project_id).values_list()
			if not p_configuration:
				template_configuration = Template_Configuration.objects.filter(template=project.template_id).values_list()
				for t in template_configuration:
					tupla = t
					name = tupla[1]
					value = tupla[2]
					p = Project_Configuration(name = name,
								value = value,
								project_id = project_id
								)
					p.save()
				p_configuration = Project_Configuration.objects.filter(project=project_id).values_list()
			
			form_configuration = Project_ConfigurationForm(p_configuration)
			return render_to_response('project.html', {'form' : form,
						'project_id' : project_id,
						'project' : project.name,
						'form_configuration' : form_configuration})
		else:
			projects = Project.objects.all()
			print 'Lista de projetos: %s ' % projects
			return render_to_response('project_list.html', { 'projects' : projects })


#create or list a project configuration
def project_create(request, project_id=0):

	if project_id > 0: #list projects configurations
		return project(request, project_id)
	else:
		form = ProjectForm()
		
	return render_to_response('project.html', {'form' : form})


#saves a project configuration
def project_configuration_save(request):
	if request.method == 'POST':
		for ids in request.POST.keys():
			project_configuration = Project_Configuration.objects.get(id=ids)
			project_configuration.value = request.POST[ids]
			project_configuration.save()
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	else:
		return HttpResponse("configuration not commited")
		
#manage project stages
def project_stage(request, project_id=0):
	#POST
	if request.method == 'POST':
		form = StageForm(request.POST)
		if form.is_valid():
			name_var = request.POST['name']
			raw_password = request.POST['password']
			password_var = ''
			s = Stage.objects.filter(project=project_id, name=name_var)
			p = Project.objects.filter(id=project_id)
			project_name = p[0].name
			if s:
				form = StageForm(project_id)
				return render_to_response('stage.html', {'form' : form, 
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
						password = raw_password,
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
				return render_to_response('stage.html', {'form' : form, 
							'project_name' : project_name,
							'stage' : name_var, 
							'project' : project_name, 
							'project_id' : project_id,
							'stage_table' : stage_table})
		else:
			return HttpResponse("form is not valid")
	#GET
	else:
		stage = Stage.objects.filter(project=project_id)
		if stage:
			#return HttpResponse("list stages")
			stage_table = StageTable(stage)
			user = stage[0].user
			deploy_to = stage[0].deploy_to
			form = StageForm(initial={'user' : user, 'deploy_to' : deploy_to})
			p = Project.objects.filter(id=project_id)
			project_name = p[0].name
			return render_to_response('stage.html', {'form' : form, 
						'project' : project_name,
						'project_id' : project_id,
						'stage_table' : stage_table})
		else:
			p = Project.objects.filter(id=project_id)
			if p:
				p_configuration = Project_Configuration.objects.filter(project=project_id)
				p_dict = name_value_dict(p_configuration)
				user = p_dict['config.fab_user']
				deploy_to = p_dict['config.deploy_to']
				form = StageForm(initial={'user' : user, 'deploy_to' : deploy_to})
				project_name = p[0].name
				return render_to_response('stage.html', {'form' : form, 
							'project' : project_name,
							'project_id' : project_id})
			else:
				return HttpResponse('<h2>Project does not exists</h2>')

			
#manage project tasks
def project_fabfile(request, project_id=0):
	#POST
	if request.method == 'POST':
		pass
	#GET
	else:
		stage = Stage.objects.filter(project=project_id)
		if stage:
			project = Project.objects.get(id=project_id)
			if project:
				fabfile = Fabfile.objects.filter(project=project_id)
				#check if there is any fabfifle for the project
				if fabfile:
					#return HttpResponse("<h1>TODO: generate form form fabfile</h1>")
					name = fabfile[0].name
					body = fabfile[0].body
					form = FabfileForm(initial={'name' : name, 'fabfile' : body, 'project_id' : project_id})
					return render_to_response('fabfile.html', {'form' : form, 
								'project_id' : project_id,
								'project' : project.name})
				else:
					#gets fabfile from the template
					fabfile_template = Fabfile_Template.objects.filter(template=project.template_id)
					p_configuration = Project_Configuration.objects.filter(project=project_id)
					p_dict = name_value_dict(p_configuration)

					#saves tasks templates in the database for the respective project
					task_template_dir = settings.TASKS_TEMPLATE_DIR
					for x in xrange(len(fabfile_template)):
						id = fabfile_template[x].id
						name = fabfile_template[x].name
						description = fabfile_template[x].description
						file_ = fabfile_template[x].file
						template_file = task_template_dir + '/' + file_
						print 'reading template file: %s' % template_file
						file_template = None
						body = None
						try:
							file_template = open(template_file, 'r')
							body = file_template.read()
							print 'done'
						finally:
							file_template.close()
							print 'template file %s closed' % template_file
						body = render_to_string('tasks/' + file_, { 'application_name' : p_dict['config.application'],
								'default_tag' : p_dict['default_tag'],
								'default_clone' : p_dict['default_clone'],
								'deploy_to' : p_dict['config.deploy_to'],
								'appdjango' : p_dict['config.appdjango'],
								'releases_to_keep' : p_dict['config.releases_days_to_keep']})
						#saves template data in database
						new_fabfile = Fabfile(name=name, body=body, project=project)
						new_fabfile.save()
					return HttpResponseRedirect(request.META['HTTP_REFERER'])
			else:
				return HttpResponse("<h1>Project does not exists!</h1>")
		else:
			return HttpResponse("<h1>You must create a stage before</h1>")
			

#saves a project configuration
def project_fabfile_save(request, project_id=0):
	if request.method == 'POST':
		fabfile = Fabfile.objects.get(project=project_id)
		body = request.POST['fabfile']
		fabfile.body = body
		fabfile.save()
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	else:
		return HttpResponse("configuration not commited")

#view the fabfile with syntax highlight
def project_fabfile_view(request, project_id=0):
	if request.method == 'GET':
		fabfile = Fabfile.objects.get(project=project_id)
		return render_to_response('fabfile.html', {'fabfile' : fabfile.body})
	else:
		return HttpResponse("not a GET")

def project_list(request):
	pass
	#GET
	if request.method == 'GET':
		pass
	#POST
	elif request.method == 'POST':
		pass

#view the fabfile with syntax highlight
def project_manage(request, project_id=0):
	#GET
	if request.method == 'GET':
		#TODO: cache on memcache
		project = Project.objects.get(id=project_id)
		fabfile = Fabfile.objects.get(project=project_id)
		stage = Stage.objects.filter(project=project_id).values_list()
		STAGE_LIST = []
		TASKS_LIST = []
		for x in xrange(len(stage)):
			STAGE_LIST.append(stage[x][0:2])
		print 'stages for project_id %s: %s' % (project_id, STAGE_LIST)
		#get tasks from fabfile
		#TODO: cache this
		fabfile_body = fabfile.body
		lines = fabfile_body.splitlines()
		i = 0
		for line in lines:
			line = line.strip()
			if line.startswith('def '):
				j = line.find('(')
				task_name = line[4:j]
				tupla = (task_name, task_name)
				TASKS_LIST.append(tupla)
				#print '%d - %s' % (i,task_name)
			i = i + 1
		print 'tasks for project_id %s: %s' % (project_id, TASKS_LIST)
		
		form = Project_ManageForm(STAGE_LIST,TASKS_LIST,initial={'project_id' : project_id})
		return render_to_response('project_manage.html', {'form' : form, 
								'project_id' : project_id,
								'project' : project.name})
	#POST
	elif request.method == 'POST':
		print 'POST received for project_id %s: %s' % (project_id, request.POST)
		task = request.POST['task']
		stage_id = request.POST['stage']
		print 'task: %s' % task
		print 'stage_id: %s' % stage_id
		stage = Stage.objects.get(id=stage_id)
		stage_name = stage.name
		lista_hosts = []
		for h in str(stage.hosts).split(','):
			lista_hosts.append(str(h))
		print str(lista_hosts)
		task_description = 'stage %s' % stage.name
		#task created acording the specified stage
		stage_task = render_to_string('tasks/stage.fabfile', {'task_name' : stage.name,
								'task_description' : task_description,
								'lista_hosts' : lista_hosts,
								'fab_user' : stage.user,
								'fab_password' : stage.password,
								'deploy_to' : stage.deploy_to})
		print 'stage task: '
		print stage_task
		print ''
		##################################
		# initiate 
		#################################
		project = Project.objects.get(id=project_id)
		fabfile = Fabfile.objects.get(project=project_id)
		stage = Stage.objects.filter(project=project_id).values_list()
		fabfile_body = fabfile.body
		lines = fabfile_body.split('\n')
		i = 0
		first_task_line = 0
		#######################################
		# write fabfile on disk to be executed
		#######################################
		timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
		dir_fabfile = '/tmp/webfabric_%s' % timestamp
		#creates directory for fabfile.py
		os.mkdir(dir_fabfile)
		f = dir_fabfile + '/fabfile.py'
		f_fabfile = open(f, 'w')
		for line in lines:
			f_fabfile.write(line.replace('\r','') + '\n')
			if line.startswith('def '):
				if first_task_line == 0:
					first_task_line = i
				j = line.find('(')
				task_name = line[4:j]
				#print '%d - %s' % (i,task_name)
			i = i + 1
		f_fabfile.write(stage_task.replace('\r','') + '\n')
		f_fabfile.close()
		print 'fabfile writed on %s ' % f
		print 'first task ocurred at %d' % first_task_line
		lines.insert(first_task_line - 1, stage_task)
		############################
		# executes the command
		############################
		os.chdir(dir_fabfile)
		try:
			cmdline = "fab %s %s" % (stage_name, task)
			print 'command line: %s' % cmdline
			status, output = commands.getstatusoutput(cmdline)
		finally:
			#removes the fabfile.py
			os.remove(f)
			os.rmdir(dir_fabfile)
		return render_to_response('fabric_output.html', {'status' : status,
								'output' : output})
		return HttpResponse("POST")
	else:
		return HttpResponse("only POST and GET are accepted")
		
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

#returns a dict mapping a name/value pair from project configuration
def name_value_dict(obj):
	p_dict = {}
	for x in xrange(len(obj)):
		p_dict[obj[x].name] = obj[x].value
	return p_dict

def set_password(raw_password):
	return hashlib.md5(raw_password).hexdigest()

def get_password(password):
	pass
