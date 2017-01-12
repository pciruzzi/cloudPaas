from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from containers.models import Container

import requests
import json
import sys
import subprocess

@csrf_exempt
@login_required
def index(request):
	context = {}
	current_user = request.user
	print("The current user is: ")
	print(current_user.id)
	#context = RequestContext(request)
	print("In the index")
	containers = Container.objects.filter(user = current_user)
	#containers = Container.objects.all()
	
	for c in containers:
		print(c.containerName)
	#user = context['user']
	print(current_user)
	context = {'containers':containers}
	return render(request, 'containers/index.html', context)

@csrf_exempt
@login_required
def create(request):
	BASE = "http://192.168.0.3:8083/"
	global V1
	V1 = BASE + "v1/"
	global V2_BETA
	V2_BETA = BASE + "v2-beta/"

	global HOSTS
	HOSTS = V1 + "hosts"
	global CONTAINERS
	CONTAINERS = V2_BETA + "projects/1a5/containers"

	context = {}

	if request.method == 'GET':
		data = '{"description":"Une description", "imageUuid":"docker:pciruzzi/paasinsa1617", "name":"api-test", "ports":["8094:3000/tcp"], "requestedHostId":"1h5"}'
		response = requests.post(CONTAINERS, auth=(rancherUser, rancherPassword), data=data)
		print(response.status_code)
		subprocess.Popen(['iptables', '-t', 'nat', '-A', 'PREROUTING', '-p', 'tcp', '--dport', '8094', '-j', 'DNAT', '--to-destination', '192.168.0.1:8094'])
		subprocess.Popen(['iptables-save'])
		return render(request, 'containers/create.html', context)

	elif request.method == 'POST':
		print("This is a POST")
		container = Container(user=request.user, containerType=request.POST['containerType'], 
			containerName=request.POST['containerName'])
		container.save()
		return render(request,'containers/index.html',context)

@csrf_exempt
@login_required
def change(request):
	context = {}
	if request.method == 'GET':
		return render(request, 'containers/index.html', context)

	elif request.method == 'POST':
		return render(request, 'containers/index.html', context)


@csrf_exempt
@login_required
def run(request,container_id):
	print
	context = {}
	if request.method == 'POST':
		container = Container.objects.get(id=container_id)
	return render(request, 'containers/run.html', context)

@csrf_exempt
@login_required
def stop(request, container_id):
	context = {}
	if request.method == 'POST':
		container = Container.objects.get(id=container_id)
		container.value = 0
		container.save()
		return render(request, 'containers/stop.html')
