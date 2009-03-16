from django import forms
from django.forms import ModelForm
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
	#my_field = ChoiceField(choices=[(1, 1), (2, 2)], initial=1) 
	template = forms.ChoiceField(choices=template_list)

class Project_ManageForm(forms.Form):

	def __init__(self, stage_choices=None, tasks_choices=None, *args, **kwargs):
		super(Project_ManageForm, self).__init__(*args, **kwargs)
		if stage_choices:
			#stage = forms.ChoiceField(choices=stage_choice)
			self.fields['stage'] = forms.ChoiceField(label='stage', 
							choices=stage_choices)
		else:	
			self.fields['stage'] = forms.ChoiceField(label='stage')
		
		if tasks_choices:
			self.fields['task'] = forms.ChoiceField(label='task', 
							choices=tasks_choices)
		else:
			self.fields['tasks'] = forms.ChoiceField(label='tasks')
			
		self.fields['project_id'] = forms.CharField(widget=forms.HiddenInput())

class Project_ListForm(forms.Form):

	def __init__(self, project_choices=None, *args, **kwargs):
		super(Project_ManageForm, self).__init__(*args, **kwargs)
		if stage_choices:
			#stage = forms.ChoiceField(choices=stage_choice)
			self.fields['project'] = forms.ChoiceField(label='choose a project', 
							choices=project_choices)
		else:	
			self.fields['project'] = forms.ChoiceField(label='choose a project')

		self.fields['actions'] = forms.ChoiceField(label='action', 
						choices=[('create', 'create'), ('manage','manage')])

		self.fields['project_id'] = forms.CharField(widget=forms.HiddenInput())

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

class StageForm(forms.Form):
	name = forms.CharField(label="name")
	user = forms.CharField(label="config.fab_user", widget=forms.TextInput(attrs={'size':'60'}))
	password = forms.CharField(label="config.fab_password", widget=forms.PasswordInput(attrs={'size':'60'}))
	hosts = forms.CharField(label="config.fab_hosts", widget=forms.TextInput(attrs={'size':'60'}))
	deploy_to = forms.CharField(label="config.deploy_to", widget=forms.TextInput(attrs={'size':'60'}))

class FabfileForm(forms.Form):
	name = forms.CharField()
	fabfile = forms.CharField(widget=forms.Textarea(attrs={'rows':'130','cols':'100'}))
	project_id = forms.CharField(widget=forms.HiddenInput()) 


