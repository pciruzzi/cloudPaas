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
import random

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
			port = 8090 + c.id
			link = "http://213.32.27.235:" + str(port)
			actualContainer = {
				'id' : c.id,
				'name' : c.containerName,
				'type' : c.containerType,
				'state' : c.currentState,
				'containerLink' : link
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

		# Choosing the host
		response = requests.get(settings.HOSTS, auth=(settings.RANCHER_USER, settings.RANCHER_PASS))
		jsonData = response.json()["data"]
		requestedHost = None
		bestResult = 999999
		for x in xrange(0,len(jsonData)):
			id = jsonData[x]["id"]
			infos = jsonData[x]["info"]
			memAvailable = infos["memoryInfo"]["memAvailable"]
			memTotal =  infos["memoryInfo"]["memTotal"]
			percentageMem = 100.0 * memAvailable / memTotal
			percentageDisk = infos["diskInfo"]["mountPoints"]["/dev/sda1"]["percentage"]
			cpuPercentages = infos["cpuInfo"]["cpuCoresPercentages"]
			percentageCpu = 0
			for y in xrange(0, len(cpuPercentages)):
				percentageCpu += cpuPercentages[y]
			percentageCpu = 1.0 * percentageCpu / len(cpuPercentages)
			result = percentageMem + percentageCpu + percentageDisk
			if ((result < bestResult) and (percentageMem < 80) and (percentageDisk < 80) and (percentageCpu < 80)):
				bestResult = result
				requestedHost = id
		# A good host hasn't been found
		if (requestedHost == None):
			requestedHost = jsonData[random.randint(0, len(jsonData) - 1)]["id"]

		if (containerType == "C Platform"):
		    print("C platform")
		    imageId = "paasinsa1617/cimage"
		elif (containerType == "Java Platform"):
		    print("Java platform")
		    imageId = "paasinsa1617/javaeeimage"
		elif (containerType == "Big data Platform"):
		    print("Big data platform")	
		    imageId = "paasinsa1617/bigdataimage"
		elif (containerType == "Web Development"):
		    print("Web development") 
		    imageId = "paasinsa1617/webdevimage"
		
		hash_object = hashlib.sha224(str(port).encode())
		containerPassword = hash_object.hexdigest()
		containerPassword = containerPassword[:8]
		link = "213.32.27.235:" + str(port)

		jsonMessage = {
				'message' : '1',
				'password' : containerPassword,
				'containerLink' : link,
			}

		# Volume creation
		data = '{"description":"Description :)", "driver":"rancher-nfs", "name":"' + volumeName + '", "driverOpts": { }}'
		response = requests.post(settings.VOLUMES, auth=(settings.RANCHER_USER, settings.RANCHER_PASS), data=data)
		jsonResponse = response.json()
		container.volumeId = jsonResponse["id"]
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
			port = 8090 + container.id
			link = "http://213.32.27.235:" + str(port)
			print(response.status_code)
			container.save()
			jsonMessage = {
				'message' : '1',
				'containerLink': link,
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
		container = Container.objects.get(user_id = user.id, id = container_id)
		URI = settings.CONTAINERS + "/" + container.rancherId
		response = requests.delete(URI, auth=(settings.RANCHER_USER, settings.RANCHER_PASS))
		URI = settings.VOLUMES + "/" + container.volumeId
		print(URI)
		response = requests.delete(URI, auth=(settings.RANCHER_USER, settings.RANCHER_PASS))
		print(response.status_code)
		container.delete()
		jsonMessage = {
				'message' : '1'
			}
		return JsonResponse(jsonMessage)
