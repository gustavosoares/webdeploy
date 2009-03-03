from django import forms
from deploy.admin.widgets import AdminDateWidget
from deploy.admin.widgets import AdminTimeWidget

#FORMS
TEMPLATE_CHOICE = ( 
		('none', '-----------------'),
	)
class ProjectForm(forms.Form):
    name = forms.CharField(initial="Nome do projeto")
    description = forms.CharField()
    creation_date = forms.CharField(widget=AdminDateWidget())
    creation_time = forms.CharField(widget=AdminTimeWidget())
    Template = forms.ChoiceField(choices=TEMPLATE_CHOICE)