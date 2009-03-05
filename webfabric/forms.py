from django import forms
from django.forms import ModelForm
from deploy.admin.widgets import AdminDateWidget
from deploy.admin.widgets import AdminTimeWidget
from deploy.webfabric.models import Template
from deploy.webfabric.models import Template_Configuration
from deploy.webfabric.models import Project_Configuration
#FORMS

class ProjectForm(forms.Form):
	name = forms.CharField()
	description = forms.CharField()
	creation_date = forms.CharField(widget=AdminDateWidget())
	creation_time = forms.CharField(widget=AdminTimeWidget())
	#retorna array com tuplas
	#CHOICES_LIST = [('0', '----------')]
	template_list = Template.objects.all().values_list()
	#for l in template_list:
		#CHOICES_LIST.append(l)
	template = forms.ChoiceField(choices=template_list)

class Project_ConfigurationForm(ModelForm):
	class Meta:
		model = Project_Configuration
	
