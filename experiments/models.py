from django.db import models
from django.contrib.auth.models import User
from corpora.models import *
from lm.models import *
from util import files
import re, math
from django.utils import timezone
from collections import defaultdict
import subprocess

SURPRISAL_GRAPH_SIZE = 30

class Experiment(models.Model):
    RUNNING = 1
    FINISHED = 2
    STATUS_CHOICES = (
        (1, 'Running'),
        (2, 'Finished'),
    )
    
    TEST_CORPUS = 1
    INPUT_TEXT = 2
    TYPE_CHOICES = (
        (1, 'Test corpus'),
        (2, 'Input text'),
    )
    
    user = models.ForeignKey(User)
    lm = models.ForeignKey(LM)
    test_corpus = models.ForeignKey(Corpus, blank=True, null=True)
    text_path = models.CharField(max_length=300)
    experiment_set = models.ForeignKey('ExperimentSet', blank=True, null=True)
    
    date_run = models.DateTimeField('date published')
    experiment_type = models.IntegerField(choices=STATUS_CHOICES, default=1)
    status = models.IntegerField(choices=TYPE_CHOICES, default=1)

    startWordIndex = 0
    endWordIndex = 29
    totalWords = 29
    maxWord = 30

    def get_indices(self):
        return [self.startWordIndex, self.endWordIndex, self.totalWords - 2]

    def corpus_name(self):
        if self.experiment_type == self.TEST_CORPUS:
            return self.test_corpus.name
        else:
            return "Inputted text"

    # Return the full contents of the results file
    def results_file(self):
        path = files.experiment_results_file_path(self)
        return files.file_contents(path)
    
    # Get the last line of the results file
    def lsvlm_results(self):
        lsvlm_output = files.tail(files.experiment_results_file_path(self), 2).strip()
        #lsvlm_output = lsvlm_output.split("\n")
	split = re.findall(r"([A-Za-z ]+:? ([0-9\.]+( \(\d+.\d+%\))?|-nan))", lsvlm_output)
        stats = [s[0].strip().replace(":", "").replace(" (", "(").rsplit(" ", 1) for s in split]
        results = {}
        for [key, value] in stats : results[key] = value
        return results

    def total_score(self):
        return self.lsvlm_results()['Total Score']

    def perplexity(self):
        return self.lsvlm_results()['Perplexity']

    def total_words(self):
        return self.lsvlm_results()['Total number of words']

    def in_voc(self):
        return self.lsvlm_results()['InVoc']

    def not_scored(self):
        return self.lsvlm_results()['Not Scored']

    def oov(self):
        return self.lsvlm_results()['OOV']

    def search_results(self, searchword = ""):
        full_results = []
        path = files.experiment_results_file_path(self)
        excerpt = subprocess.check_output(["grep", "-n", searchword, path]).split("\n")
        for line in excerpt :
            if (len(line) > 0):
                line = line.strip().split(":")
                full_results.append(int(line[0]))
        return full_results

    def get_contexts(self, results):
        path = files.experiment_results_file_path(self)
        contextStart = []
        contextEnd = []
        for num in results:
            if (num < 11):
                num = 11
            elif (num > self.totalWords() - 11):
                num = self.totalWords - 1
            excerptStart = subprocess.check_output(["sed", "-n", str(num-10) + "," + str(num - 1) + "p", path]).split("\n")
            excerptEnd = subprocess.check_output(["sed", "-n", str(num+1) + "," + str(num+10) + "p", path]).split("\n")
            for line in excerptStart:
                contextStart.append(line.split()[0])
            for line in excerptEnd:
                contextEnd.append(line.split()[0])
        return contextStart, contextEnd

    # Get the text results to display in the output
    def text_results(self, index, searchword=""):
        path = files.experiment_results_file_path(self)
        full_results = []
        if (searchword == ""):
            excerpt = subprocess.check_output(["sed", "-n", str(index+1) + "," + str(index + 33) + "p", path]).split("\n")
            for line in excerpt :
                line = line.strip()
                if len(line) > 0: full_results.append(line)
            full_results.pop()
            full_results.pop()
            try:
                labels, values = zip(*[s.strip().rsplit(None, 1) for s in full_results])
            except ValueError :
                labels = []
                values = []
            else :
                values = [v if v == '***OOV***' else (abs(float(v))) for v in values]
            return [labels, {self.lm.name:values}]
        else:
            excerpt = subprocess.check_output(["grep", "-n", searchword, path]).split("\n")
            for line in excerpt :
                if (len(line) > 0):
                    line = line.strip().split(":")
                    full_results.append(int(line[0]))
            return full_results
    
    def corpus_location(self):
        if(self.experiment_type == self.INPUT_TEXT):
            return self.text_path
        else:
            return self.test_corpus.file_path()
    
class ExperimentSet(models.Model):
    user = models.ForeignKey(User)
    
    lms = models.ManyToManyField(LM)
    corpora = models.ManyToManyField(Corpus)
    
    date_run = models.DateTimeField('date published')
    
    TEST_CORPUS = 1
    INPUT_TEXT = 2
    TYPE_CHOICES = (
        (1, 'Test corpora'),
        (2, 'Input text'),
    )

    startWordIndex = 0
    endWordIndex = 29
    totalWords = 29
    
    experiment_type = models.IntegerField(choices=TYPE_CHOICES, default=1)

    def get_indices(self):
        return [self.startWordIndex, self.endWordIndex, self.totalWords + 1]

    def corpora_names(self):
        if self.experiment_type == self.TEST_CORPUS:
            return ", ".join([corpus.name for corpus in self.corpora.all()])
        else:
            return "Inputted text"
    
    def lm_names(self):
        return ", ".join([lm.name for lm in self.lms.all()])
    
    def status_text(self):
        if(self.finished()):
            return "Finished"
        else:
            return "Running..."
    
    def finished(self):
        return (not self.experiment_set.filter(status=Experiment.RUNNING).exists())

    def generate_input_experiments(self, corpus_location):
        for lm in self.lms.all():
            exp = Experiment(user=self.user, date_run=timezone.now(), lm=lm, text_path=corpus_location,
                                experiment_type=Experiment.INPUT_TEXT, experiment_set=self)
            exp.save()
        
    def generate_corpora_experiments(self):
        for lm in self.lms.all():
            for corpus in self.corpora.all():
                exp = Experiment(user=self.user, date_run=timezone.now(), lm=lm, test_corpus=corpus,
                                experiment_type=Experiment.TEST_CORPUS, experiment_set=self)
                exp.save()

    def search_results(self, searchword = ""):
        for exp in self.experiment_set.all():
            return exp.search_results(searchword)

    def context_results(self, results):
        for exp in self.experiment_set.all():
            return exp.get_context(results)

    def text_results(self, index = 0, searchWord = ""):
        values = {}
        labels = []
	corp = []

        for exp in self.experiment_set.all():
            output = exp.text_results(index, searchWord)
            if (searchWord != ""):
                return output
            [self.startWordIndex, self.endWordIndex, self.totalWords] = exp.get_indices()
            if exp.corpus_name() not in corp:
		labels += output[0]
		corp.append(exp.corpus_name())
            if exp.lm.name not in values : values[exp.lm.name] = []
            #values[exp.lm.name] += output[1][exp.lm.name][:SURPRISAL_GRAPH_SIZE]
            #labels = tuple(labels[:SURPRISAL_GRAPH_SIZE])
            values[exp.lm.name] += output[1][exp.lm.name]
            labels = tuple(labels)
        return [labels, values]

    def lsvlm_results(self):
        results = []
        for exp in self.experiment_set.all():
            if exp.experiment_type == ExperimentSet.INPUT_TEXT : corpus = "Input Text"
            else : corpus = exp.test_corpus.name
            output = exp.lsvlm_results()
            result = [exp.id, corpus, exp.lm.name]
            for stat in output : result.append(stat[1])
            results.append(result)
        return results
