from django.shortcuts import render
from index.models import *
from django.core.urlresolvers import reverse
import time
import os
import subprocess
import json
from django.core import serializers


from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

import socket

ip = socket.gethostbyname(socket.gethostname())
port = 9000


#ANALYSİS


#Views.py kodları asagıda

@login_required
def form(request):
	return render(request, "index/upload.html", {})

@login_required
def homePage(request):
	return render(request, "index/home.html", {})

@login_required
def results(request):
	mail = request.user.email
	projectNames = FinishedProjects.objects.filter(USERMAIL=mail).order_by().values_list('PROJECT', flat=True).distinct()
	projectNames = json.dumps(list(projectNames))
	return render(request, "index/results.html", {"projectNames" : projectNames,"ip":ip,"port":port})

@login_required
def download(request):
	mail = request.user.email
	projectNames = FinishedProjects.objects.filter(USERMAIL=mail).order_by().values_list('PROJECT', flat=True).distinct()
	projectNames = json.dumps(list(projectNames))
	return render(request, "index/download.html", {"projectNames" : projectNames,"mail":mail,"ip":ip,"port":port})

@login_required
def getFileData(request,query):
	mail = request.user.email
	fileNames = FinishedProjects.objects.filter(USERMAIL=mail).filter(PROJECT = query).order_by().values_list('FILE', flat=True)
	fileNames = json.dumps(list(fileNames))
	return JsonResponse(fileNames, safe=False)

@login_required
def getVarData(request,query):
	[projectName,fileName] = query.split("|;*:|")
	mail = request.user.email
	results = Results.objects.filter(USERMAIL=mail).filter(PROJECT = projectName).filter(FILE = fileName)
	results = serializers.serialize('json', results)
	results = json.dumps(results)
	return JsonResponse(results, safe=False)

@login_required
def getDownloadContent(request,query):
	downloadContent = []
	[projectName,fileName] = query.split("|;*:|")
	mail = request.user.email
	path = 'media//' + mail + '//' + projectName
	fileList = os.listdir(path)
	for record in fileList:
		if fileName in record:
			downloadContent.append(record)
	return JsonResponse(downloadContent, safe=False)

@login_required
def analysisInformation(request):
	mail = request.user.email
	projects = Project.objects.filter(mail=request.user.email)
	projects = serializers.serialize('json', projects)
	projects = json.dumps(projects)
	return render(request, "index/analysisInformation.html", {"projects" : projects, "ip":ip, "port":port})

@login_required
def getProjectInfo(request):
	mail = request.user.email
	projects = Project.objects.filter(mail=request.user.email)
	projects = serializers.serialize('json', projects)
	projects = json.dumps(projects)
	return JsonResponse(projects, safe=False)

@login_required
def removeFile(request, filename=None):
	try:
		os.remove('media//' + request.user.email + '//' + 'entrance' + '//' + filename)
		print (filename + ' removed')
	except:
		print('nope')
	return HttpResponseRedirect('/upload')


@login_required
def startAnalysis(request, project=None):
	readType = project.split(":;")[1]
	project = project.split(":;")[0]
	try:
		os.makedirs('media//'+request.user.email + '//' + project)
	except:
		print('error creating project folder')

	fileList = os.listdir('media//'+request.user.email+'//'+'entrance')
	for file in fileList:
		try:
			os.rename('media//' + request.user.email + '//' + 'entrance' + '//' + file, 'media//' + request.user.email + '//' + project + '//' + file)
			Input.objects.create(user = request.user, mail = request.user.email, fileName = file, groupName = project, sam = False, bam = False, vcf = False, annotation = False)
			print (file + ' moved')
		except:
			print('file cannot be moved')
	subprocess.Popen(["python3", "index//startAnalysis.py",request.user.email,project,readType])
	now = time.localtime()
	today = time.strftime("%d/%m/%y %H:%M:%S", now)
	Project.objects.create(user = request.user, mail = request.user.email, name = project, start = today, stop = False, ending = 0, readType = readType)

	return HttpResponseRedirect('/form')


@login_required
def upload(request):
	now = time.localtime()
	today = time.strftime("%d/%m/%y", now)
	for count, x in enumerate(request.FILES.getlist("files")):
		def process(f):
			try:
				os.makedirs('media//'+request.user.email)
				print(request.user.email + ' folder created')
			except:
				pass
			try:
				os.makedirs('media//'+request.user.email+'//'+'entrance')
				print(request.user.email + '/entrance folder created')
			except:
				pass
			with open('media//'+request.user.email+'//'+'entrance'+'//' + str(x),'wb+' ) as destination:
				for chunk in f.chunks():
					destination.write(chunk)
		process(x)
	filesList = os.listdir('media//'+request.user.email+'//'+'entrance')
	folderList = os.listdir('media//'+request.user.email+'//')
	return render(request, "index/upload.html", {'filesList': filesList,'folderList':folderList})

@login_required
def delete(request):
	a = reverse('del')
	redirect('views.upload')


def login(request):
	if request.user.is_authenticated():
		return render(request, 'index/login.html', {'user':request.user})
	else:
		if request.method == 'POST':
			username = request.POST['user']
			password = request.POST['pass']

			user = authenticate(username=username, password=password)
			if user:
				if user.is_active:
					auth_login(request, user)
					try:
						os.makedirs('media//'+request.user.email)
						print(request.user.email + ' folder created')
					except:
						pass
					try:
						os.makedirs('media//'+request.user.email+'//'+'entrance')
						print(request.user.email + '/entrance folder created')
					except:
						pass
					return HttpResponseRedirect('/')
				else:
					return HttpResponse("Hesap aktif değil, lütfen iletişime geçin.")
			else:
				print("Kullanıcı adı veya şifre hatalı, belki de böyle bir kullanıcı yoktur.")
				return HttpResponse("Kullanıcı adı veya şifre hatalı, belki de böyle bir kullanıcı yoktur")
	return render(request, 'index/login.html')




@login_required
def logout(request):
	auth_logout(request)
	return HttpResponseRedirect('/form')
