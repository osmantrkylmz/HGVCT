from django.db import models

# Create your models here.
class Input (models.Model):
    user = models.TextField()
    mail = models.TextField()
    fileName = models.TextField()
    groupName = models.TextField()
    sam = models.TextField()
    bam = models.TextField()
    vcf = models.TextField()
    annotation = models.TextField()

class Project (models.Model):
    user = models.TextField()
    mail = models.TextField()
    name = models.TextField()
    start = models.TextField()
    stop = models.TextField()
    ending = models.TextField()
    readType = models.TextField()


class Results (models.Model):
    CHROM = models.TextField()
    POS = models.TextField()
    REF = models.TextField()
    ALT = models.TextField()
    RS = models.TextField()
    GT = models.TextField()
    GENE = models.TextField()
    DP = models.TextField()
    VARTYPE = models.TextField()
    EFFECT = models.TextField()
    IMPACT = models.TextField()
    HGVS_C = models.TextField()
    PROJECT = models.TextField()
    FILE = models.TextField()
    USERMAIL = models.TextField()

class FinishedProjects (models.Model):
    PROJECT = models.TextField()
    FILE = models.TextField()
    USERMAIL = models.TextField()
