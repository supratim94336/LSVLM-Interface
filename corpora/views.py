from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from corpora.models import Corpus, Lang, CountFile
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from corpora.corpus_form import CorpusForm, CorpusEditForm
from util import files
import os

# Display an index of corpora and the Add Corpus form
@login_required
def index(request):
    corpora = Corpus.objects.all()
    langs = Lang.objects.all()
    context = {'my_corpora' : Corpus.objects.filter(user=request.user),
               'other_corpora' : Corpus.objects.exclude(user=request.user),
               'langs' : langs}

    if request.method == 'GET':
	if 'q' in request.GET :
            query = request.GET['q']
            context['my_corpora'] = context['my_corpora'].filter(label__contains=query)
            context['other_corpora'] = context['other_corpora'].filter(label__contains=query)

    if request.method == "POST":
        form = CorpusForm(request.POST, request.FILES)
        if form.is_valid():
            path_type = form.cleaned_data["path_type"]
            
            if (path_type == "file_upload"):
                name = form.cleaned_data["name"]
                file = form.cleaned_data["upload_path"]
                path = files.write_tmp_file(file, name)
            else:
                location = form.cleaned_data["location"].strip("/")
                file_name = form.cleaned_data["file_name"].strip("/")
                path = os.path.join(location, file_name)
            
            
            sample = files.corpus_sample(path, 15)
            size = files.file_size(path)
            wc = files.wc(path)
            context = {'form' : form, 'sample' : sample, 'size' : size, 'wc' : wc}
            return render(request, 'corpora/confirm_upload.html', context)
        else:
            context["form"] = form
    else:
        context["form"] = CorpusForm()
    return render(request, 'corpora/index.html', context)

# Display a corpus
@login_required
def corpus(request, corpus_id):
    corpus = Corpus.objects.get(id=corpus_id)
    sample_text = corpus.sample(15)
    corpus_size = corpus.current_size()
    corpus_wc =   corpus.wc()
    context = {'corpus'     : corpus, 
               'sample_text': sample_text,
               'corpus_size': corpus_size,
               'corpus_wc'  : corpus_wc}
    return render(request, 'corpora/corpus.html', context)
    
@login_required
def edit(request, corpus_id):
    corpus = Corpus.objects.get(id=corpus_id)
    if request.method == "POST":
        form = CorpusEditForm(request.POST, instance=corpus)
        if form.is_valid():
            form.save(commit=False)
            lang_id = form.cleaned_data["lang_select"]
            if(lang_id == "new"):
                new_lang = form.cleaned_data["new_lang"]
                corpus.lang = Lang.objects.create(name=new_lang)
            else:
                corpus.lang = Lang.objects.get(id=lang_id)
            corpus.save()
            return HttpResponseRedirect(reverse("corpora:corpus", kwargs={"corpus_id" : corpus.id}))
        else:
            context = {'corpus' : corpus, 'form' : form }
            return render(request, 'corpora/edit.html', context)
    else:
        context = {'corpus' : corpus, 'form' : CorpusEditForm(instance=corpus) }
        return render(request, 'corpora/edit.html', context)

@login_required
def purge(request, corpus_id):
    corpus = Corpus.objects.get(id=corpus_id)
    for count_file in corpus.countfile_set.all():
        os.remove(files.count_file_webserver_path(count_file))
    os.remove(files.corpus_path(corpus))
    return delete(request, corpus_id)

@login_required
def delete(request, corpus_id):
    corpus = Corpus.objects.get(id=corpus_id)
    corpus.delete()
    return HttpResponseRedirect(reverse("corpora:index"))

# Save the confirmed corpus
@login_required
def confirm(request):
    form = CorpusForm(request.POST, request.FILES)
    
    # so it passes validation
    form.fields["upload_path"].initial = True

    if form.is_valid():

        c = Corpus(user = request.user, date_added = timezone.now())
        c.name = form.cleaned_data["name"]
        c.description = form.cleaned_data["description"]
        c.process_steps = form.cleaned_data["process_steps"]
        c.metadata_url = form.cleaned_data["metadata_url"]
        
        lang_id = form.cleaned_data["lang_select"]

        if(lang_id == "new"):
            new_lang = form.cleaned_data["new_lang"]
            c.lang = Lang.objects.create(name=new_lang)
        else:
            c.lang = Lang.objects.get(id=lang_id)

        #To take value of the label field from form to the database label field
        c.label = c.name + " " + str(c.lang) + " " + str(c.user) + " " + form.cleaned_data["label"]
        
        path_type = form.cleaned_data["path_type"]
        
        if (path_type == "file_upload"):
            (c.location, c.file_name) = files.save_tmp_file(c.name)
        else:
            c.location = form.cleaned_data["location"].strip("/")
            c.file_name = form.cleaned_data["file_name"].strip("/")

        # To find out the size of the corpora
        #name2 = c.name + ".txt"
        #c.size = c.current_size()

        #To find out the word count of the corpora
        '''count = 0
        with open(files.corpus_path(c),'r') as f:
            for line in f:
                for word in line.split():
                    count+=1

        c.count = count'''
        #c.count = c.wc()

        c.save()
        return HttpResponseRedirect(reverse("corpora:corpus", kwargs={"corpus_id" : c.id}))
        
    # we should ideally never get here, so just redirect to the main index
    # in case something unexpected went wrong
    else:
        return HttpResponseRedirect(reverse("corpora:index"))

# Download the count file
@login_required
def count_file(request, count_file_id):
    count_file = CountFile.objects.get(id=count_file_id)
    
    response = HttpResponse(count_file.count_file(), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="' + count_file.corpus.name + '.txt.M' + str(count_file.m) + '"'
    return response
