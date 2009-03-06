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
			
	
