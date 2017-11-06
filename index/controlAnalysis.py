import time
import os
import sys
import django
import json
from django.core import serializers
import re
import subprocess
import psutil


sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE']='upload.settings'
django.setup()

from index.models import *

cpu = 70
ram = 70

media= os.getcwd() + "/media/"

projectData = Project.objects.all()
projectData = serializers.serialize('json', projectData)
projectData = json.loads(projectData)

for project in projectData:
	if project["fields"]["stop"] == "False" and int(project["fields"]["ending"]) < 500:
		mail = project["fields"]["mail"]
		readType = project["fields"]["readType"]
		project = project["fields"]["name"]
		path = media + mail + '//' + project+"//"
		for fileName in os.listdir(path):
			if not fileName.endswith("fastq.gz") or fileName.endswith("fastq"):
				os.remove(path + fileName)
			else:
				Input.objects.filter(mail=mail).filter(groupName=project).update(sam = False, bam = False, vcf = False, annotation = False)

				ccc = FinishedProjects.objects.filter(USERMAIL = mail).filter(PROJECT = project)
				aaa = serializers.serialize('json', ccc)
				aaa = json.loads(aaa)
				print(aaa)
				ccc.delete()
				ddd = Results.objects.filter(USERMAIL = mail).filter(PROJECT = project)
				bbb = serializers.serialize('json', ddd)
				bbb = json.loads(bbb)
				print(bbb)
				ddd.delete()

		Project.objects.filter(mail = mail).filter(name = project).update(ending = 0 )
		time.sleep(15)
		while(psutil.cpu_percent()>cpu or psutil.virtual_memory().percent > ram):
			print(project)
			time.sleep(15)
		print("osman")
		subprocess.Popen(["python3", "index//startAnalysis.py",mail,project,readType])
