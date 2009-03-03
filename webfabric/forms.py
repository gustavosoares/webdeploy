from django import forms

#FORMS
TEMPLATE_CHOICE = ( 
		('none', '-----------------'),
	)
class ProjectForm(forms.Form):
    name = forms.CharField(initial="Nome do projeto")
    description = forms.CharField()
    creation_dt = forms.DateTimeField()
    Template = forms.ChoiceField(choices=TEMPLATE_CHOICE)