from django.db import models
import django_tables as tables 

# Create your models here.
class Template(models.Model):
	name = models.CharField(max_length=100)
	
	def __unicode__(self):
		return u'%s' % (self.name)
        
class Template_Configuration(models.Model):
	name = models.CharField(max_length=255)
	value = models.CharField(max_length=255)
	template = models.ForeignKey(Template)

	def __unicode__(self):
		return u'%s' % (self.name)

class Project(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=200)
	creation_date = models.DateField()
	creation_time = models.TimeField()
	template = models.ForeignKey(Template)

	def __unicode__(self):
		return u'%s' % (self.name)

class Project_Configuration(models.Model):
	name = models.CharField(max_length=255)
	value = models.CharField(max_length=255)
	project = models.ForeignKey(Project)

	def __unicode__(self):
		return u'%s' % (self.name)
		
class Stage(models.Model):
	name = models.CharField(max_length=100)
	user = models.CharField(max_length=40) #config.fab_user
	hosts = models.CharField(max_length=500) #config.fab_hosts
	deploy_to = models.CharField(max_length=100) #config.deploy_to
	project = models.ForeignKey(Project)

	def __unicode__(self):
		return u'%s' % (self.name)

class StageTable(tables.ModelTable):  
	id = tables.Column(sortable=False, visible=False)
	name = tables.Column(name='name')
	user = tables.Column(name='config.fab_user')
	hosts = tables.Column(name='config.fab_hosts')
	deploy_to = tables.Column(name='config.deploy_to')
	class Meta:  
		model = Stage
		exclude = ['project']

class Tasks(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=500)
	body = models.TextField()
	project = models.ForeignKey(Project)

	def __unicode__(self):
		return u'%s' % (self.name)

class Tasks_Template(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=500)
	file = models.CharField(max_length=255)
	template = models.ForeignKey(Template)

	def __unicode__(self):
		return u'%s' % (self.name)