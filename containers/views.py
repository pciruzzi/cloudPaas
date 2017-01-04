from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("This will show the list of containers")

def create(request):
	return HttpResponse("This will be the create a containers view")

def run(request,container_id):
	return HttpResponse("This view will run the container #" + container_id)
