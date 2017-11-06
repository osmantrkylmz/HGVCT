import time
import os
import sys
import django

sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE']='upload.settings'
django.setup()

from index.models import *
import subprocess
import psutil

pair1 = sys.argv[1]
pair2 = sys.argv[2]
media = sys.argv[3]
path = sys.argv[4]
mail = sys.argv[5]
project = sys.argv[6]
readType = sys.argv[7]
fileCount = sys.argv[8]
core = str(int(psutil.cpu_count()/2))

now = time.localtime()
today = time.strftime("%d/%m/%y %H:%M:%S", now)
print("süre : "+today)


percPerFile = 100/int(fileCount)
percPerProcess = int(percPerFile/5)


def pairfastq2vcf(pair1,pair2,media,path,mail,project):

	sample_name = "_".join(pair1.split("_")[:-2])
	os.system("bwa mem -t " + core + " " + media+"genome/genome.fa " + path + pair1 +" "+ path + pair2 + " > " + path + sample_name+ ".sam")
	now = time.localtime()
	today = time.strftime("%d/%m/%y %H:%M:%S", now)
	Input.objects.filter(mail=mail).filter(groupName=project).filter(fileName=pair1).update(sam=today)
	Input.objects.filter(mail=mail).filter(groupName=project).filter(fileName=pair2).update(sam=today)
	completed = Project.objects.filter(mail=mail).filter(name = project).values("ending")[0]["ending"]
	Project.objects.filter(mail = mail).filter(name = project).update(ending = int(completed) + percPerProcess)
	os.system('samtools view -@ '+ core +' -Sb ' + path + sample_name+ '.sam'+ ' >' +  path + sample_name+ '.bam')
	now = time.localtime()
	today = time.strftime("%d/%m/%y %H:%M:%S", now)
	Input.objects.filter(mail=mail).filter(groupName=project).filter(fileName=pair1).update(bam=today)
	Input.objects.filter(mail=mail).filter(groupName=project).filter(fileName=pair2).update(bam=today)
	completed = Project.objects.filter(mail=mail).filter(name = project).values("ending")[0]["ending"]
	Project.objects.filter(mail = mail).filter(name = project).update(ending = int(completed) + percPerProcess)
	os.system('samtools sort -@ '+ core +' -m 2G '+ path + sample_name+'.bam' + ' -o ' + path + sample_name+ '_sorted.bam' )
	os.system('samtools index '+ path + sample_name+'_sorted.bam')
	os.system('samtools mpileup -uf ' + media+'genome/genome.fa ' + path + sample_name+'_sorted.bam' +' | ' + 'bcftools call -mvO z -o ' + path + sample_name+'.raw.bcf')
	os.system('bcftools view '+ path + sample_name+'.raw.bcf' +' | vcfutils.pl varFilter -Q30 > ' + path + sample_name+'flt.vcf')
	now = time.localtime()
	today = time.strftime("%d/%m/%y %H:%M:%S", now)
	Input.objects.filter(mail=mail).filter(groupName=project).filter(fileName=pair1).update(vcf=today)
	Input.objects.filter(mail=mail).filter(groupName=project).filter(fileName=pair2).update(vcf=today)
	completed = Project.objects.filter(mail=mail).filter(name = project).values("ending")[0]["ending"]
	Project.objects.filter(mail = mail).filter(name = project).update(ending = int(completed) + percPerProcess)
	os.system('java -Xmx8g -jar media/snpEff/SnpSift.jar annotate media/snpEff/db/GRCh38/dbSnp/All.vcf.gz ' + path + sample_name+'flt.vcf > ' +  path + sample_name+'dbsnp.vcf')
	os.system('java -Xmx8g -jar media/snpEff/SnpSift.jar annotate media/snpEff/db/GRCh38/clinvar/clinvar.vcf ' +  path + sample_name+'dbsnp.vcf > '  + path + sample_name+'clinvar.vcf')
	os.system('java -jar media/snpEff/SnpSift.jar varType ' +  path + sample_name + 'clinvar.vcf > ' + path + sample_name+'gt.vcf' )
	os.system('snpEff -v hg38 ' + path + sample_name+'gt.vcf >' + path + sample_name+'final.vcf' )
	now = time.localtime()
	today = time.strftime("%d/%m/%y %H:%M:%S", now)
	Input.objects.filter(mail=mail).filter(groupName=project).filter(fileName=pair1).update(annotation=today)
	Input.objects.filter(mail=mail).filter(groupName=project).filter(fileName=pair2).update(annotation=today)
	completed = Project.objects.filter(mail=mail).filter(name = project).values("ending")[0]["ending"]
	Project.objects.filter(mail = mail).filter(name = project).update(ending = int(completed) + percPerProcess)
	os.system('java -jar media/snpEFF/SnpSift.jar extractFields '+ path + sample_name+'final.vcf' +' CHROM POS REF ALT ID HOM \"EFF[0].GENE\" DP VARTYPE \"ANN[0].EFFECT\" \"EFF[0].IMPACT\" \"ANN[0].HGVS_C\" > ' + path + sample_name+'results.vcf')

	resFile = open(path + sample_name+'results.vcf')
	resFile = resFile.read()
	resFile = resFile.strip().split("\n")
	resFile = [i.strip().split("\t") for i in resFile[1:]]

	for var in resFile:
		[CHROM,POS,REF,ALT,RS,HOM,GENE,DP,VARTYPE,EFFECT,IMPACT,HGVS_C] = var
		if HOM == "true":
			GT = "Homozigot"
		elif HOM == "false":
			GT = "Heterozigot"
		else:
			GT = ""

		EFFECT = EFFECT.split("_")[0]
		Results.objects.create(CHROM = CHROM, POS = POS, REF = REF, ALT = ALT, RS = RS, GT = GT, GENE = GENE, DP = DP, VARTYPE = VARTYPE, EFFECT = EFFECT, IMPACT = IMPACT, HGVS_C = HGVS_C, PROJECT= project, FILE=sample_name, USERMAIL = mail )
	FinishedProjects.objects.create(PROJECT= project, FILE=sample_name, USERMAIL = mail)
	completed = Project.objects.filter(mail=mail).filter(name = project).values("ending")[0]["ending"]
	Project.objects.filter(mail = mail).filter(name = project).update(ending = int(completed) + percPerProcess)

def singlefastq2vcf(pair1,pair2,media,path,mail,project):

	sample_name = "_".join(pair1.split("_")[:-2])
	os.system("bwa mem -t "+ core + " " + media+"genome/genome.fa " + path + pair1 + " > " + path + sample_name+ ".sam")
	now = time.localtime()
	today = time.strftime("%d/%m/%y %H:%M:%S", now)
	Input.objects.filter(mail=mail).filter(groupName=project).filter(fileName=pair1).update(sam=today)
	completed = Project.objects.filter(mail=mail).filter(name = project).values("ending")[0]["ending"]
	Project.objects.filter(mail = mail).filter(name = project).update(ending = int(completed) + percPerProcess)
	os.system('samtools view -@ ' + core +' -Sb ' + path + sample_name+ '.sam'+ ' >' +  path + sample_name+ '.bam')
	now = time.localtime()
	today = time.strftime("%d/%m/%y %H:%M:%S", now)
	Input.objects.filter(mail=mail).filter(groupName=project).filter(fileName=pair1).update(bam=today)
	completed = Project.objects.filter(mail=mail).filter(name = project).values("ending")[0]["ending"]
	Project.objects.filter(mail = mail).filter(name = project).update(ending = int(completed) + percPerProcess)
	os.system('samtools sort -@ '+ core +' -m 2G '+ path + sample_name+'.bam' + ' -o ' + path + sample_name+ '_sorted.bam' )
	os.system('samtools index '+ path + sample_name+'_sorted.bam')
	os.system('samtools mpileup -uf ' + media+'genome/genome.fa ' + path + sample_name+'_sorted.bam' +' | ' + 'bcftools call -mvO z -o ' + path + sample_name+'.raw.bcf')
	os.system('bcftools view '+ path + sample_name+'.raw.bcf' +' | vcfutils.pl varFilter -Q30 > ' + path + sample_name+'flt.vcf')
	now = time.localtime()
	today = time.strftime("%d/%m/%y %H:%M:%S", now)
	Input.objects.filter(mail=mail).filter(groupName=project).filter(fileName=pair1).update(vcf=today)
	completed = Project.objects.filter(mail=mail).filter(name = project).values("ending")[0]["ending"]
	Project.objects.filter(mail = mail).filter(name = project).update(ending = int(completed) + percPerProcess)
	os.system('java -Xmx8g -jar media/snpEff/SnpSift.jar annotate media/snpEff/db/GRCh38/dbSnp/All.vcf.gz ' + path + sample_name+'flt.vcf > ' +  path + sample_name+'dbsnp.vcf')
	os.system('java -Xmx8g -jar media/snpEff/SnpSift.jar annotate media/snpEff/db/GRCh38/clinvar/clinvar.vcf ' +  path + sample_name+'dbsnp.vcf > '  + path + sample_name+'clinvar.vcf')
	os.system('java -jar media/snpEff/SnpSift.jar varType ' +  path + sample_name + 'clinvar.vcf > ' + path + sample_name+'gt.vcf' )
	os.system('snpEff -v hg38 ' + path + sample_name+'gt.vcf >' + path + sample_name+'final.vcf' )
	now = time.localtime()
	today = time.strftime("%d/%m/%y %H:%M:%S", now)
	Input.objects.filter(mail=mail).filter(groupName=project).filter(fileName=pair1).update(annotation=today)
	completed = Project.objects.filter(mail=mail).filter(name = project).values("ending")[0]["ending"]
	Project.objects.filter(mail = mail).filter(name = project).update(ending = int(completed) + percPerProcess)
	os.system('java -jar media/snpEFF/SnpSift.jar extractFields '+ path + sample_name+'final.vcf' +' CHROM POS REF ALT ID HOM \"EFF[0].GENE\" DP VARTYPE \"ANN[0].EFFECT\" \"EFF[0].IMPACT\" \"ANN[0].HGVS_C\" > ' + path + sample_name+'results.vcf')

	resFile = open(path + sample_name+'results.vcf')
	resFile = resFile.read()
	resFile = resFile.strip().split("\n")
	resFile = [i.strip().split("\t") for i in resFile[1:]]

	for var in resFile:
		[CHROM,POS,REF,ALT,RS,HOM,GENE,DP,VARTYPE,EFFECT,IMPACT,HGVS_C] = var
		if HOM == "true":
			GT = "Homozigot"
		elif HOM == "false":
			GT = "Heterozigot"
		else:
			GT = ""

		EFFECT = EFFECT.split("_")[0]
		Results.objects.create(CHROM = CHROM, POS = POS, REF = REF, ALT = ALT, RS = RS, GT = GT, GENE = GENE, DP = DP, VARTYPE = VARTYPE, EFFECT = EFFECT, IMPACT = IMPACT, HGVS_C = HGVS_C, PROJECT= project, FILE=sample_name, USERMAIL = mail )
	FinishedProjects.objects.create(PROJECT= project, FILE=sample_name, USERMAIL = mail)
	completed = Project.objects.filter(mail=mail).filter(name = project).values("ending")[0]["ending"]
	Project.objects.filter(mail = mail).filter(name = project).update(ending = int(completed) + percPerProcess)

if (readType == "pair"):
	pairfastq2vcf(pair1,pair2,media,path,mail,project)
else:
	singlefastq2vcf(pair1,pair2,media,path,mail,project)
