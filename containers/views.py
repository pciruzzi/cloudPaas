from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
@login_required
def index(request):
	context = {}
	return render(request, 'containers/index.html', context)

@csrf_exempt
@login_required
def create(request):

	context = {}

	if request.method == 'GET':
		return render(request, 'containers/create.html', context)

	elif request.method == 'POST':
		print("This is a POST")
		return render(request,'containers/index.html',context)

@csrf_exempt
@login_required
def run(request,container_id):
	context = {}
	return render(request, 'containers/run.html', context)
