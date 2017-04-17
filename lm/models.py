import os
from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField
from corpora.models import Corpus
from util import files
#from sets import Set
from util import qsub, files

# Create your models here.
class LM(models.Model):
    UNTRAINED = 1
    TRAINED = 2
    TRAINING = 3
    STATUS_CHOICES = (
        (1, 'Untrained'),
        (2, 'Trained'),
        (3, 'Training'),
    )
    
    name = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User)
    description = models.CharField(max_length=500)
    date_added = models.DateTimeField('date published')
    last_trained = models.DateTimeField(null=True, blank=True)
    lmdata = JSONField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    default_corpus = models.IntegerField(default=0)

    def __str__(self):
        return self.name
        
    def train(self):
        qsub.train_lm(self)
    
    # output of the arpa file
    def arpa_file(self):
        path = files.arpa_file_path(self)
        return files.file_contents(path)
        
    # output the .lm file in text
    def lm_file(self):
        path = files.lm_file_path(self)
        return files.file_contents(path)
