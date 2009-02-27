from django.db import models

# Create your models here.
class Configuration(models.Model):
	name = models.CharField(max_length=255)
	value = models.CharField(max_length=255)
	fabfile = models.TextField()


class Template(models.Model):
	name = models.CharField(max_length=100)
	configuration = models.ForeignKey(Configuration)

class Project(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=200)
	creation_dt = models.DateTimeField()
	template = models.ForeignKey(Template)
#	environment = models.ManyToManyField(Environment)

class Environment(models.Model):
	name = models.CharField(max_length=100)
	hosts = models.CharField(max_length=500)
	project = models.ForeignKey(Project)

