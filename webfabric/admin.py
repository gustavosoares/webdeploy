from django.contrib import admin
from models import *

class TemplateAdmin(admin.ModelAdmin):
	pass

class Template_ConfigurationAdmin(admin.ModelAdmin):
	list_display = ('template', 'name', 'value')
	list_filter = ('template', 'name')
	ordering = ('-template',)

class EnvironmentAdmin(admin.ModelAdmin):
	pass

class ProjectAdmin(admin.ModelAdmin):
	pass

class Project_ConfigurationAdmin(admin.ModelAdmin):
	pass

#admin.site.register(Template, TemplateAdmin)
admin.site.register(Template_Configuration, Template_ConfigurationAdmin)
admin.site.register(Environment, EnvironmentAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Project_Configuration, Project_ConfigurationAdmin)