from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Container(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)	
	diskSpace = models.DecimalField(max_digits=10, decimal_places=2, default=-1
		, blank=True, null=True)
	cpu = models.DecimalField(max_digits=10, decimal_places=2, default=-1
		, blank=True, null=True)
	ram = models.DecimalField(max_digits=10, decimal_places=2, default=-1
		, blank=True, null=True)
	creationDate = models.DateField(auto_now_add=True)
	lastBackUp = models.DateTimeField(auto_now= True)
	currentServer = models.IntegerField(default=-1
		, blank=True, null=True)
	containerType = models.CharField(max_length=250)
	currentState = models.IntegerField(default=0)
	containerName = models.CharField(max_length=250, default='Container')
	containerAddress = models.CharField(max_length=250, default='test')
	rancherId = models.CharField(max_length=50, default='')