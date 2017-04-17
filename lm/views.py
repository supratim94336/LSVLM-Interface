from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from corpora.models import Corpus, Lang
from lm.models import LM
from util import qsub, files
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from lm import language_models
import json, os

@login_required
def index(request):
    context = { 'my_lms' : LM.objects.filter(user = request.user),
                'other_lms': LM.objects.exclude(user = request.user)}
    return render(request, 'lm/index.html', context)

@login_required
def new(request):
    lm_id = -1
    context = {'lm_id' : lm_id, 'editing' : False,
               'language_models' : language_models.lms, 'corpora' : Corpus.objects.all(),
               'save_text' : "Save LM", 'save_url' : reverse('lm:save')}   
    return render(request, 'lm/new.html', context)

@login_required
def edit(request, lm_id):
    context = {'lm' : LM.objects.get(id=lm_id), 'editing' : True, 
               'language_models' : language_models.lms, 'corpora' : Corpus.objects.all(), 
               'save_text' : "Save LM", 'save_url' : reverse('lm:save', args=[lm_id])}
    return render(request, 'lm/new.html', context)

# TODO: display error message on the original page if this doesn't work for some reason
@login_required
def save(request, lm_id=-1):
    name = request.POST.get("name")
    description = request.POST.get("description")
    json_data = json.loads(request.POST.get("lm_json"))
    default_corpus = request.POST.get("default_corpus")

    if lm_id == -1 :
        lm_obj = LM(name=name, description=description, lmdata=json_data, user=request.user,date_added=timezone.now(),
                    default_corpus=default_corpus)
        lm_obj.save()
        files.make_lm_dir(lm_obj.id)

    else :
        lm_obj = LM.objects.get(id=lm_id)
        files.remove_lm_files(lm_obj)
        files.make_lm_dir(lm_id)
        lm_obj.name = name
        lm_obj.description = description
        lm_obj.lmdata = json_data
        lm_obj.status = LM.UNTRAINED
        lm_obj.default_corpus = default_corpus
        lm_obj.save()

    countsfiles = {}
    output = "# Parameters 1\n"
    output += "MainLM\tMainLM\n"
    for key, data in lm_obj.lmdata[0].items():
        output += "# LMDefinition " + str(len(data)) + "\n"
        output += "Name\t" + key + "\n"
        for field, value in data.items():
            # The coordinates and default LM
            # are saved so we can reconstruct the LM in the browser,
            # but don't output them in the LM file
            if (field=="coords" or field=="default_lm"):
                continue
            if isinstance(value, list):
                if(value[0] == 'lm'):
                    output += field + "\t" + str(value[1]) + "\n"
                elif(value[0] == 'corpus'):
                    if "M" in data : n = str(data["M"])
		    else : n = "1"
                    if value[1] in countsfiles : 
                        countsfiles[value[1]].add(n)
                    else : countsfiles[value[1]] = set([n])
                    #value.append("2")
                    output += "Tree\tTree" + value[1] + "_" + n + "\n"
            else:
                output += field + "\t" + str(value) + "\n"

    for corpus in countsfiles:
        c = Corpus.objects.get(id=corpus)
        for n in countsfiles[corpus]:
            output += "# TreeDefinition 2\n"
            output += "Name\tTree" + corpus + "_" + str(n) + "\n"
            tree_file = c.file_name + ".M" + str(n) + ".cnt"
            output += "File " + os.path.join(files.CLUSTER_GUI_DIR, files.TREE_PATH, str(c.id), tree_file) + "\n"

    files.write_lm_file(lm_obj.name, lm_obj.id, output)
    return HttpResponseRedirect(reverse("lm:lm", kwargs={"lm_id" : lm_obj.id }))

@login_required
def lm(request, lm_id):
    context = {'lm' : LM.objects.get(id=lm_id)}
    return render(request, 'lm/lm.html', context)
    
@login_required
def lm_file(request, lm_id):
    lm = LM.objects.get(id=lm_id)
    response = HttpResponse(lm.lm_file(), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="' + lm.name + '.lm"'
    return response

@login_required
def train(request, lm_id):
    lm = LM.objects.get(id=lm_id)
    
    qsub.train_lm(lm)
    lm.status = LM.TRAINING
    lm.save()
    
    return HttpResponseRedirect(reverse("lm:lm", kwargs={"lm_id" : lm.id }))

@login_required
def arpa_file(request, lm_id):
    lm = LM.objects.get(id=lm_id)
    
    response = HttpResponse(lm.arpa_file(), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="' + lm.name + '.arpa"'
    return response

@login_required
def purge(request, lm_id):
    lm = LM.objects.get(id=lm_id)
    files.remove_lm_files(lm)
    return delete(request, lm_id)

@login_required
def delete(request, lm_id):
    lm = LM.objects.get(id=lm_id)
    lm.delete()
    return HttpResponseRedirect(reverse("lm:index"))

@login_required
def copy(request, lm_id):
    lm = LM.objects.get(id=lm_id)
    lm.pk = None
    lm.name = lm.name + " (Copy)"
    lm.user = request.user
    lm.date_added=timezone.now()
    lm.last_trained = None
    lm.status = LM.UNTRAINED
    lm.save()
    
    return HttpResponseRedirect(reverse("lm:lm", kwargs={"lm_id" : lm.id }))
