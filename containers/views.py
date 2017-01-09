from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from containers.models import Container

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

	context = {}

	if request.method == 'GET':
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
