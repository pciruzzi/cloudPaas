from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from containers.models import Container
from django.contrib.auth.models import User
from django.conf import settings

import requests
import json
import sys
import subprocess
import hashlib

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


		port = 8090 + container.id
		volumeName = "VolumeApi" + str(port)
		requestedHost = "1h5"
		imageId = "pciruzzi/paasinsa1617"

		hash_object = hashlib.sha1(str(port))
		containerPassword = hash_object.hexdigest()
		containerPassword = containerPassword[:8]

		jsonMessage = {
				'message' : '1',
				'password' : containerPassword
			}

		# Volume creation
		data = '{"description":"Description :)", "driver":"rancher-nfs", "name":"' + volumeName + '", "driverOpts": { }}'
		response = requests.post(settings.VOLUMES, auth=(settings.RANCHER_USER, settings.RANCHER_PASS), data=data)
		print(response.status_code)

		# Container creation
		data = '{"description":"Une description", "imageUuid":"docker:' + imageId + '", "name":"api-test' + str(port) + '", "ports":["' + str(port) + ':3000/tcp"], "requestedHostId":"' + requestedHost + '", "dataVolumes":["' + volumeName + ':/datas"], "environment":{ "DOCKER_USER": "' + username + '", "DOCKER_PASS":"' + containerPassword + '" }}'
		response = requests.post(settings.CONTAINERS, auth=(settings.RANCHER_USER, settings.RANCHER_PASS), data=data)
		print(response.status_code)
		jsonResponse = response.json()
		container.rancherId = jsonResponse["id"]
		container.save()
		subprocess.Popen(['iptables', '-t', 'nat', '-A', 'PREROUTING', '-p', 'tcp', '--dport', str(port), '-j', 'DNAT', '--to-destination', '192.168.0.1:' + str(port)])
		subprocess.Popen(['iptables-save'])


		return JsonResponse(jsonMessage)

@csrf_exempt
#@login_required
def change(request):
	print("in colkjd")
	context = {}
	if request.method == 'GET':
		return render(request, 'containers/change.html', context)

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
			URI = settings.CONTAINERS + "/" + container.rancherId + "?action=start"
			response = requests.post(URI, auth=(settings.RANCHER_USER, settings.RANCHER_PASS))
			print(response.status_code)
			container.save()
			jsonMessage = {
				'message' : '1'
			}
		elif (container.currentState == 1):
			container.currentState = 0
			data = '{"remove":"false", "timeout":10}'
			URI = settings.CONTAINERS + "/" + container.rancherId + "?action=stop"
			response = requests.post(URI, auth=(settings.RANCHER_USER, settings.RANCHER_PASS), data=data)
			print(response.status_code)
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
