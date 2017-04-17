from django.db import models
from django.contrib.auth.models import User
from util import files
import os


# Name of the language of the corpus
class Lang(models.Model):
    name = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.name

# Corpus
class Corpus(models.Model):
    class Meta:
        verbose_name_plural = "corpora"
    user = models.ForeignKey(User)
    date_added = models.DateTimeField('date published')
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500)
    process_steps = models.CharField(max_length=500)
    location = models.CharField(max_length=300)
    file_name = models.CharField(max_length=200)
    metadata_url = models.CharField(max_length=300)
    size = models.CharField(max_length=300, default = '0') #new field for size of corpora
    count = models.CharField(max_length=300, default = '0') #new field for count of corpora
    label = models.CharField(max_length=100, default = '0') # new field for tag search

    lang = models.ForeignKey(Lang)
    
    def file_path(self):
        return os.path.join(self.location, self.file_name)
    
    def sample(self, num_lines):
        return files.corpus_sample(self.file_path(), num_lines)

    def current_size(self):
        return files.file_size(self.file_path())
    
    def wc(self):
        return files.wc(self.file_path())

    def __str__(self):
        return self.name
    
    @property
    def date_added_str(self):
        return self.date_added.strftime("%Y-%m-%d")


class CountFile(models.Model):
    corpus = models.ForeignKey(Corpus)
    m = models.IntegerField()

    def file_name(self):
        return self.corpus.file_name + ".M" + str(self.m) + ".cnt"
    
    def count_file(self):
        path = files.count_file_path(self)
        return files.file_contents(path)
    
class Meta:
    unique_together = ('corpus', 'm',)
