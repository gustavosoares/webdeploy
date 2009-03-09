from django import forms
from django.conf import settings
from django.forms import ModelForm
from django.template.loader import render_to_string
from deploy.admin.widgets import AdminDateWidget
from deploy.admin.widgets import AdminTimeWidget
from deploy.webfabric.models import Template
from deploy.webfabric.models import Template_Configuration
from deploy.webfabric.models import Project_Configuration
from deploy.webfabric.models import Stage
#FORMS

class ProjectForm(forms.Form):
	name = forms.CharField()
	description = forms.CharField(widget=forms.TextInput(attrs={'size':'60'}))
	creation_date = forms.CharField(widget=AdminDateWidget())
	creation_time = forms.CharField(widget=AdminTimeWidget())
	#retorna array com tuplas
	template_list = Template.objects.all().values_list()
	template = forms.ChoiceField(choices=template_list)

'''
class Project_ConfigurationForm(ModelForm):
	class Meta:
		model = Project_Configuration
'''


class Project_ConfigurationForm(forms.Form):
	def __init__(self, project, *args, **kwargs):
		super(Project_ConfigurationForm, self).__init__(*args, **kwargs)
		p_configuration = None
		
		if type(project).__name__ == 'ValuesListQuerySet':
			p_configuration = project
		else :
			p_configuration = Project_Configuration.objects.filter(project=project_id).values_list()
		for p_item in p_configuration:
			p_aux = p_item
			id = p_aux[0]
			name = p_aux[1]
			value = p_aux[2]
			self.fields[id] = forms.CharField(label=name, 
							initial=value,
							widget=forms.TextInput(attrs={'size':'60'})
							)


class Create_StageForm(forms.Form):
	name = forms.CharField(label="name")
	user = forms.CharField(label="config.fab_user", widget=forms.TextInput(attrs={'size':'60'}))
	hosts = forms.CharField(label="config.fab_hosts", widget=forms.TextInput(attrs={'size':'60'}))
	deploy_to = forms.CharField(label="config.deploy_to", widget=forms.TextInput(attrs={'size':'60'}))

class StageForm(forms.Form):
	def __init__(self, project_arg = None, *args, **kwargs):
		super(StageForm, self).__init__(*args, **kwargs)	
		if type(project_arg).__name__ == 'ValuesListQuerySet':
			stage = Stage.objects.filter(project=project_arg).values_list()
			for s_item in stage:
				s_aux = s_item
				id = s_aux[0]
				name = s_aux[1]
				user = s_aux[2]
				hosts = s_aux[3]
				deploy_to = s_aux[4]
				self.fields[id] = forms.CharField(label=name, 
							initial=value,
							widget=forms.TextInput(attrs={'size':'60'})
							)
		elif type(project_arg).__name__ == 'unicode':
			p_configuration = Project_Configuration.objects.filter(project=project_arg, name='config.deploy_to')
			self.fields['name'] = forms.CharField(label="name")
			self.fields['user'] = forms.CharField(label="config.fab_user", widget=forms.TextInput(attrs={'size':'60'}))
			self.fields['hosts']= forms.CharField(label="config.fab_hosts", widget=forms.TextInput(attrs={'size':'60'}))
			self.fields['deploy_to'] = forms.CharField(label="config.deploy_to", 
								widget=forms.TextInput(attrs={'size':'60'}),
								initial=p_configuration[0].value)
		elif type(project_arg).__name__ == 'NoneType':
			self.fields['name'] = forms.CharField(label="name")
			self.fields['user'] = forms.CharField(label="config.fab_user", widget=forms.TextInput(attrs={'size':'60'}))
			self.fields['hosts']= forms.CharField(label="config.fab_hosts", widget=forms.TextInput(attrs={'size':'60'}))
			self.fields['deploy_to'] = forms.CharField(label="config.deploy_to", 
								widget=forms.TextInput(attrs={'size':'60'}))
'''
Method for generating the task form. It may receive 2 arguments. A queryset, which retrieved from the tasks_template tables
and the other one is a dict with a key-value pair from the values obtained from the project_configuration tables. This two
arguments are just used when there is no task creates for the project_id received, this means, only on the first time.
'''
class TasksForm(forms.Form):
	def __init__(self, obj = None, project = None, *args, **kwargs):
		super(TasksForm, self).__init__(*args, **kwargs)	
		if type(obj).__name__ == 'QuerySet':
			task_template_dir = settings.TASKS_TEMPLATE_DIR
			for x in xrange(len(obj)):
				id = obj[x].id
				name = obj[x].name
				description = obj[x].description
				file_ = obj[x].file
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
					body = render_to_string('tasks/' + file_, { 'application_name' : project['config.application'],
										'default_tag' : project['default_tag'],
										'default_clone' : project['default_clone'],
										'deploy_to' : project['config.deploy_to'],
										'appdjango' : project['config.appdjango'],
										'releases_to_keep' : project['config.releases_days_to_keep']})
				self.fields[id] = forms.CharField(label=name, 
							initial=body,
							widget=forms.Textarea(attrs={'rows':'20','cols':'100'}))
		elif type(project_arg).__name__ == 'NoneType':
			self.fields['name'] = forms.CharField(label="name")
			self.fields['description'] = forms.CharField(label="description", widget=forms.TextInput(attrs={'size':'60'}))
			self.fields['body']= forms.TextField()

