import os
import sys
import psutil
import time
import subprocess
import smtplib
from email.mime.text import MIMEText


import django

cpu = 70
ram = 70

sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE']='upload.settings'
django.setup()

from index.models import *

email = sys.argv[1]
projectName = sys.argv[2]
readType = sys.argv[3]
media= os.getcwd() + "/media/"
print(media)
def sendMail(receiverMail,project):
	account="geneanalyse@gmail.com"
	password = 'qweQWE123'

	to = receiverMail            # alıcının mail adresi
	subject = project +' Analiz Sonucu'
	body = project+ ' analziniz bitmistir. Sonuclari inceleyebilirsiniz!'



	mail = MIMEText(body, 'html', 'utf-8')
	mail['From'] = account
	mail['Subject'] = subject
	mail['To'] = to
	mail = mail.as_string()

	try:
		server = smtplib.SMTP('smtp.gmail.com:587')   #servere bağlanmak için gerekli host ve portu belirttik
		server.ehlo()
		server.starttls() #serveri TLS(bütün bağlantı şifreli olucak bilgiler korunucak) bağlantısı ile başlattık
		server.login(account, password)   # Gmail SMTP server'ına giriş yaptık
		server.sendmail(account, to, mail) # Mail'imizi gönderdik
		server.close()     # SMTP serverimizi kapattık
		print ('email gönderildi')
	except:
		print("bir hata oluştu")


def pairedEndList(mail,project,media,readType):
	print("burda")
	path = media + mail + '//' + project+"//"
	match_list=[]
	file_list = []
	for file in os.listdir(path):
		if file.endswith(".fastq.gz"):
			file_list.append(file)

	for i in range(0, len(file_list)):
		for j in range(0, len(file_list)):
			temp= set(file_list[i].split('_'))-set(file_list[j].split('_'))
			if  'R1' in temp and len(temp)==1:
				sub_list=[]
				sub_list.append(file_list[i])
				sub_list.append(file_list[j])
				match_list.append(sub_list)
	print (match_list)
	for pair in match_list:
		loop = True
		while(psutil.cpu_percent()>cpu or psutil.virtual_memory().percent > ram):
			time.sleep(15)
		subprocess.Popen(["python3", 'index/'+"fastq2vcf.py",pair[0],pair[1],media,path,mail,project,readType,str(len(match_list))])

	completed = 0
	while(completed < len(match_list)):
		completed = 0
		for pair in match_list:
			annotation = Input.objects.filter(mail=mail).filter(groupName=project).filter(fileName=pair[0]).values("annotation")[0]["annotation"]
			if annotation != "False":
				completed = completed + 1
				print("ano : " +annotation)
			print("completed = "+ str(completed) )
		time.sleep(1)
	print("bitti")
	now = time.localtime()
	today = time.strftime("%d/%m/%y %H:%M:%S", now)
	Project.objects.filter(mail = mail).filter(name = project).update(stop = today )
	Project.objects.filter(mail = mail).filter(name = project).update(ending = 100 )
	sendMail(email,project)

def singleEndList(mail,project,media,readType):
	print("burda")
	path = media + mail + '//' + project+"//"
	match_list=[]
	file_list = []
	for file in os.listdir(path):
		if file.endswith(".fastq.gz"):
			file_list.append(file)

	print (file_list)
	for readFile in file_list:
		loop = True
		while(psutil.cpu_percent()>cpu or psutil.virtual_memory().percent > ram):
			time.sleep(15)
		subprocess.Popen(["python3", 'index/'+"fastq2vcf.py",readFile,readFile,media,path,mail,project,readType,str(len(file_list))])

	completed = 0
	while(completed < len(file_list)):
		completed = 0
		for readFile in file_list:
			annotation = Input.objects.filter(mail=mail).filter(groupName=project).filter(fileName=readFile).values("annotation")[0]["annotation"]
			if annotation != "False":
				completed = completed + 1
				print("ano : " +annotation)
			print("completed = "+ str(completed) )
		time.sleep(1)
	print("bitti")
	now = time.localtime()
	today = time.strftime("%d/%m/%y %H:%M:%S", now)
	Project.objects.filter(mail = mail).filter(name = project).update(stop = today )
	Project.objects.filter(mail = mail).filter(name = project).update(ending = 100 )
	sendMail(email,project)

if (readType == "pair"):
	pairedEndList(email,projectName,media,readType)
else:
	singleEndList(email,projectName,media,readType)
