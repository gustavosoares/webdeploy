from django.db import models

# Create your models here.
class Template(models.Model):
	name = models.CharField(max_length=100)
	
	def __unicode__(self):
		return u'%s' % (self.name)
        
class Configuration(models.Model):
	name = models.CharField(max_length=255)
	value = models.CharField(max_length=255)
	template = models.ForeignKey(Template)
	#fabfile = models.TextField()

	def __unicode__(self):
		return u'%s' % (self.name)

class Project(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=200)
	creation_dt = models.DateTimeField()
	template = models.ForeignKey(Template)
	
#	environment = models.ManyToManyField(Environment)
	def __unicode__(self):
		return u'%s' % (self.name)

class Environment(models.Model):
	name = models.CharField(max_length=100)
	hosts = models.CharField(max_length=500)
	project = models.ForeignKey(Project)

	def __unicode__(self):
		return u'%s' % (self.name)
