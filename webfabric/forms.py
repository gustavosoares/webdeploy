from django import forms
from deploy.admin.widgets import AdminDateWidget
from deploy.admin.widgets import AdminTimeWidget
from deploy.webfabric.models import Template
#FORMS

class ProjectForm(forms.Form):
    name = forms.CharField(initial="Nome do projeto")
    description = forms.CharField()
    creation_date = forms.CharField(widget=AdminDateWidget())
    creation_time = forms.CharField(widget=AdminTimeWidget())
    #retorna array com tuplas
    CHOICES_LIST = [('0', '----------')]
    template_list = Template.objects.all().values_list()
    for l in template_list:
        CHOICES_LIST.append(l)
    template = forms.ChoiceField(choices=CHOICES_LIST)