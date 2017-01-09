from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Container(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)	
	diskSpace = models.DecimalField(max_digits=10, decimal_places=2)
	cpu = models.DecimalField(max_digits=10, decimal_places=2)
	ram = models.DecimalField(max_digits=10, decimal_places=2)
	creationDate = models.DateField(auto_now_add=True)
	currentServer = models.IntegerField()
	containerType = models.IntegerField()
	currentState = models.IntegerField()