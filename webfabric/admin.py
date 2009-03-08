from django.contrib import admin
from models import *

class TemplateAdmin(admin.ModelAdmin):
	pass

class Template_ConfigurationAdmin(admin.ModelAdmin):
	list_display = ('template', 'name', 'value')
	list_filter = ('template', 'name')
	ordering = ('-template',)


class StageAdmin(admin.ModelAdmin):
	pass

class Project_ConfigurationInline(admin.TabularInline):
	model = Project_Configuration

class ProjectAdmin(admin.ModelAdmin):
	pass

class Project_ConfigurationAdmin(admin.ModelAdmin):
	pass

class TasksAdmin(admin.ModelAdmin):
	pass

class Tasks_TemplateAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'file')
	list_filter = ('name',)
	ordering = ('-template',)
	
admin.site.register(Template, TemplateAdmin)
admin.site.register(Template_Configuration, Template_ConfigurationAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Project_Configuration, Project_ConfigurationAdmin)
admin.site.register(Tasks, TasksAdmin)
admin.site.register(Tasks_Template, Tasks_TemplateAdmin)
