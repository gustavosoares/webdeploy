from django.contrib import admin
from models import *


class ConfigurationAdmin(admin.ModelAdmin):
	pass

class TemplateAdmin(admin.ModelAdmin):
	pass

class EnvironmentAdmin(admin.ModelAdmin):
	pass

class ProjectAdmin(admin.ModelAdmin):
	pass

admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(Environment, EnvironmentAdmin)
admin.site.register(Project, ProjectAdmin)