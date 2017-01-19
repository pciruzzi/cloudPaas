from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from containers.models import Container
from django.contrib.auth.models import User

import requests
import json
import sys
import subprocess

@csrf_exempt
#@login_required
def index(request):
	if request.method == 'GET':
		context = {}
		current_user = request.user
		print("The current user is: ")
		print(current_user.id)
		print("In the index")
		containers = Container.objects.filter(user_id = current_user.id)
		for c in containers:
			print(c.containerName)
		context = {'containers':containers}
		return render(request, 'containers/index.html', context)
	elif request.method == 'POST':
		print("lsdkfjmqsdklfjsmdlfk")
		receivedData = json.loads(request.body.decode("utf-8"))
		username = receivedData["username"]
		#username = request.POST["username"]
		print(username)
		user = User.objects.get(username = username)
		containers = Container.objects.filter(user_id = user.id)
		print(containers)
		
		response = {}
		containersJson = []

		for c in containers:
			actualContainer = {
				'id' : c.id,
				'name' : c.containerName,
				'type' : c.containerType,
				'state' : c.currentState,
			}
			print(actualContainer)
			containersJson.append(actualContainer)
			#response[c.id] = actualContainer

		response = JsonResponse(containersJson, safe = False)
		print(response)

		#print(containersJson)
		return (response)

@csrf_exempt
#@login_required
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
	global VOLUMES
	VOLUMES = V2_BETA + "projects/1a5/volumes"

	global RANCHER_USER
	RANCHER_USER = "" # FILL ME
	RANCHER_PASS = ""

	context = {}

	if request.method == 'GET':
		return render(request, 'containers/create.html', context)

	elif request.method == 'POST':
		print("This is a POST")
		receivedData = json.loads(request.body.decode("utf-8"))
		username = receivedData["username"]
		print(username)
		containerType = receivedData["type"]
		containerName = receivedData["name"]
		print("before user get")
		user = User.objects.get(username = username)
		print(user)

		container = Container(user_id=user.id, containerType=containerType, 
			containerName=containerName)
		container.save()
		jsonMessage = {
				'message' : '1'
			}


		port = 8090 + container.id
		volumeName = "VolumeApi" + str(port)
		requestedHost = "1h5"
		imageId = "pciruzzi/paasinsa1617"

		# Volume creation
		data = '{"description":"Description :)", "driver":"rancher-nfs", "name":"' + volumeName + '", "driverOpts": { }}'
		response = requests.post(VOLUMES, auth=(RANCHER_USER, RANCHER_PASS), data=data)
		print(response.status_code)

		# Container creation
		data = '{"description":"Une description", "imageUuid":"docker:' + imageId + '", "name":"api-test' + str(port) + '", "ports":["' + str(port) + ':3000/tcp"], "requestedHostId":"' + requestedHost + '", "dataVolumes":["' + volumeName + ':/datas"]}'
		response = requests.post(CONTAINERS, auth=(RANCHER_USER, RANCHER_PASS), data=data)
		print(response.status_code)
		subprocess.Popen(['iptables', '-t', 'nat', '-A', 'PREROUTING', '-p', 'tcp', '--dport', str(port), '-j', 'DNAT', '--to-destination', '192.168.0.1:' + str(port)])
		subprocess.Popen(['iptables-save'])


		return JsonResponse(jsonMessage)

@csrf_exempt
#@login_required
def change(request):
	print("in colkjd")
	context = {}
	if request.method == 'GET':
		return render(request, 'containers/index.html', context)

	elif request.method == 'POST':
		#print("post")
		receivedData = json.loads(request.body.decode("utf-8"))
		username = receivedData["username"]
		container_id = receivedData["containerId"]
		user = User.objects.get(username = username)
		#print(user.id)
		container = Container.objects.get(user_id = user.id, id = container_id)
		#print(container_id)
		if (container.currentState == 0):
			container.currentState = 1
			container.save()
			jsonMessage = {
				'message' : '1'
			}
		elif (container.currentState == 1):
			container.currentState = 0
			container.save()
			jsonMessage = {
				'message' : '1'
			}
		else:
			jsonMessage = {
				'message' : '-1'
			}
		response = JsonResponse(jsonMessage, safe = False)
		return response
		#return render(request, 'containers/index.html', context)


@csrf_exempt
#@login_required
def backup(request):
	context = {}
	if request.method == 'POST':
		print("post")
		receivedData = json.loads(request.body.decode("utf-8"))
		username = receivedData["username"]
		container_id = receivedData["containerId"]
		user = User.objects.get(username = username)
		container = Container.objects.get(user_id = user.id, id = container_id)
		print("after json get")
		#now = datetime.datetime.now()
		#print(now)
		container.save()
		jsonMessage = {
				'message' : '1',
				'backupTime' : container.lastBackUp
			}
		return JsonResponse(jsonMessage)


@csrf_exempt
#@login_required
def delete(request):
	print("in delete")
	context = {}
	if request.method == 'POST':
		print("post")
		receivedData = json.loads(request.body.decode("utf-8"))
		username = receivedData["username"]
		container_id = receivedData["containerId"]
		user = User.objects.get(username = username)
		container = Container.objects.filter(user_id = user.id, id = container_id).delete()
		jsonMessage = {
				'message' : '1'
			}
		return JsonResponse(jsonMessage)
