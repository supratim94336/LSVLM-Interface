import os, string, re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms
from lm.models import LM
from util import files, qsub
from django.utils import timezone
from corpora.models import Corpus
from experiments.models import Experiment, ExperimentSet
from experiments.run_exp_form import ExperimentSetForm

@login_required
def index(request):
    context = {'lms'           : LM.objects.filter(status=LM.TRAINED), 
               'corpora'       : Corpus.objects.all(), 
               'my_expsets'    : ExperimentSet.objects.filter(user=request.user), 
               'other_expsets' : ExperimentSet.objects.exclude(user = request.user)}

    if request.method == "POST":
        form = ExperimentSetForm(request.POST, request.FILES)
        if form.is_valid():
            lm_ids = request.POST.getlist("lm")
            lms = LM.objects.filter(id__in=lm_ids)
    
            source = request.POST.get("source")
            exp_set = ExperimentSet(user=request.user, date_run=timezone.now())
            exp_set.save()
            for lm in lms: exp_set.lms.add(lm)

            files.make_experiment_dir(exp_set.id)
    
            if source == "input_text":
                exp_set.experiment_type = ExperimentSet.INPUT_TEXT
                exp_set.save()
                text = request.POST.get("input_text")
                corpus_location = files.write_experiment_corpus(exp_set.id, text)
                exp_set.generate_input_experiments(corpus_location)
            elif source == "corpus":
                exp_set.experiment_type = ExperimentSet.TEST_CORPUS
                c_ids = request.POST.getlist("corpus")
                corpora = Corpus.objects.filter(id__in=c_ids)
                for corpus in corpora: exp_set.corpora.add(corpus)
                exp_set.save()
                exp_set.generate_corpora_experiments()
            else:
                return HttpResponseRedirect(reverse("experiments:index"))
    
            for exp in exp_set.experiment_set.all():
                qsub.run_perplexity(exp)

            return HttpResponseRedirect(reverse("experiments:experiment_set", kwargs={"experiment_id" : exp_set.id}))

        else: context["form"] = form
    else: context["form"] = ExperimentSetForm()
    return render(request, 'experiments/index.html', context)

wordIndex = 0
exp_id = 0
searchWordIndex = 0
refreshInd = 0

@login_required
def concordance_click(request, row_num):
    global wordIndex
    wordIndex = int(row_num)
    return experiment_set(request, exp_id)

@login_required
def experiment_set(request, experiment_id):
    global exp_id
    global wordIndex
    global searchWordIndex
    global refreshInd
    exp_set = ExperimentSet.objects.get(id=experiment_id)
    if exp_id != exp_set.id:
        wordIndex = 0
    exp_id = exp_set.id
    context = {'experiment' : exp_set,
               'exp_set_id' : exp_set.id,
               'lm_names' : exp_set.lm_names(),
               'corpora_names' : exp_set.corpora_names() }

    if(request.GET.get('searchNumber')):
        try:
            wordIndex = int(request.GET.get('searchNumber'))
            searchWordIndex = wordIndex
        except:
            wordIndex = searchWordIndex
    elif(request.GET.get('prevBtn')):
        wordIndex -= 30
    elif(request.GET.get('nextBtn')):
        wordIndex += 30
    else:
        wordIndex = 1
    if (wordIndex < 1):
        wordIndex = 1

    if not exp_set.finished():
        context["training"] = True
    else:
        #if exp_set.experiment_type == ExperimentSet.INPUT_TEXT :
        if(request.GET.get('searchBtn')):
            results = exp_set.search_results(str(request.GET.get('searchWord')))
            [contextStart, contextEnd] = exp_set.context_results(results)
            context["search_text_results"] = results
            context["context_start"] = contextStart
            context["context_end"] = contextEnd
            context["searchWord"] = request.GET.get('searchWord')
        context["input_text_results"] = exp_set.text_results(wordIndex)
        [start, end, total] = exp_set.get_indices()
        context["startWordIndex"] = start + 1,
        context["endWordIndex"] = end + 1,
        context["totalWords"] = total + 1,
        context["exp_list"] = exp_set.experiment_set.all()
        context["lms"] = exp_set.lms.all()
        context["corpora"] = exp_set.corpora.all()
        context["refreshInd"] = "refreshed"

    if wordIndex < 15:
        wordIndex = 15
    elif wordIndex > total:
        wordIndex = total
    return render(request, 'experiments/experiment.html', context)

@login_required
def experiment(request, experiment_id):
    exp = Experiment.objects.get(id=experiment_id)
    context = {'experiment' : exp,
               'lm_names' : [exp.lm.name],
               'corpora_names' : [exp.corpus_name()] }

    if not exp.FINISHED:
        context["training"] = True

    else:
        #if exp_set.experiment_type == ExperimentSet.INPUT_TEXT : 
        context["input_text_results"] = exp.text_results()
        context["indices"] = exp.get_indices()
        context["exp_list"] = [exp]
        context["lms"] = [exp.lm]
        context["corpora"] = [exp.test_corpus]
    return render(request, 'experiments/experiment.html', context)

# Download the results file
@login_required
def results_file(request, experiment_id):
    exp = Experiment.objects.get(id=experiment_id)
    response = HttpResponse(exp.results_file(), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="results.txt"'
    return response

@login_required
def purge(request, experiment_id):
    exp_set = ExperimentSet.objects.get(id=experiment_id)
    files.remove_exp_set_files(exp_set)
    return delete(request, experiment_id)

@login_required
def delete(request, experiment_id):
    exp_set = ExperimentSet.objects.get(id=experiment_id)

    while len(exp_set.experiment_set.all()) > 0 :
        exp_set.experiment_set.first().delete()
    exp_set.delete()

    return HttpResponseRedirect(reverse("experiments:index"))