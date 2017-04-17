"""
        Utility functions for qsub
"""

from util.files import *
from corpora.models import Corpus, CountFile
import os, subprocess, re, time

CREATE_TREE_SCRIPT = os.path.join(CLUSTER_GUI_DIR, SCRIPTS_PATH, "make_trees.sh")
CREATE_ARPA_SCRIPT = os.path.join(CLUSTER_GUI_DIR, SCRIPTS_PATH, "make_arpa.sh")
PERPLEXITY_SCRIPT  = os.path.join(CLUSTER_GUI_DIR, SCRIPTS_PATH, "run_perplexity.sh")
COMBINE_SCRIPT     = os.path.join(CLUSTER_GUI_DIR, SCRIPTS_PATH, "combine_counts.sh")
VOCABULARY_SCRIPT  = os.path.join(CLUSTER_GUI_DIR, SCRIPTS_PATH, "combine_vocab.sh")

def train_lm(lm):
    """
        Train the LM by first creating all of the necessary corpus trees,
        then creating the .arpa file.
    """
    # Get a list of all of the corpora	
    countsfiles = {}
    for key, data in lm.lmdata[0].items():
        for field, value in data.items():       
            if isinstance(value, list):
                if(value[0] == 'corpus'):
                    if "M" in data : n = data["M"]
                    else : n = 1
                    if value[1] in countsfiles : 
                        countsfiles[value[1]].add(n)
                    else : countsfiles[value[1]] = set([n])

    # Make the trees for each corpus
    lm_prefix = os.path.join(CLUSTER_GUI_DIR, LM_PATH, str(lm.id), file_name(lm.name)) + ".voc"
    vocabs = [lm_prefix]
    job_names = []
    for corpus_id in countsfiles:
        c = Corpus.objects.get(id=corpus_id)
        vocab_file = os.path.join(CLUSTER_GUI_DIR, TREE_PATH, str(c.id), c.file_name) + ".voc"
        vocabs.append(vocab_file)
        for n in countsfiles[corpus_id] :
            job_name = "corpus_{0}_{1}".format(str(c.id), str(n))
            train_corpus_count(c, n, job_name)
            job_names.append(job_name)

    # Make language model vocabulary file 
    job_name = "vocab_{0}".format(str(lm.id))
    qsub_call(VOCABULARY_SCRIPT, vocabs, job_name, job_names)
    job_names.append(job_name)

    # Generate the .arpa file too
    train_arpa_file(countsfiles, lm, job_names)

def train_corpus_count(corpus, m, job_name):
    """
        Create a corpus tree for the given corpus.
        Returns the job ID.
    """
    
    # first, check if we already have a count file

    #existing_count_files = CountFile.objects.filter(corpus=corpus)
    #for cf in existing_count_files :
    #    if cf.m >= m : return None

    try:
        count_file = CountFile.objects.get(corpus=corpus, m=m)
        return None
    
    except CountFile.DoesNotExist:
        directory = os.path.join(WEBSERVER_GUI_DIR, TREE_PATH, str(corpus.id))
        subprocess.call(["mkdir -m 777 " + directory], shell=True)
        prefix = '"' + os.path.join(CLUSTER_GUI_DIR, TREE_PATH, str(corpus.id), corpus.file_name) + '"'
        corpus_location = os.path.join(CLUSTER_BASE, corpus.file_path())
        
        # Takes arguments: corpus_location: the address of the corpus
        # prefix:
        # M: the m-value for the count file
        # corpus_id: the id of the corpus (so we can create the count file afterwards)
        return qsub_call(CREATE_TREE_SCRIPT, [corpus_location, prefix, str(m), str(corpus.id)], job_name)

def train_arpa_file(countsfiles, lm, job_names):
    """
        Run the script to create a .arpa file with the given LM, n, and corpus
        job_names is the list of the job names of the corpora trees that need to be trained first
    """

    lm_prefix = os.path.join(CLUSTER_GUI_DIR, LM_PATH, str(lm.id), file_name(lm.name))
    counts = [lm_prefix + ".voc", lm_prefix]

    for corpus_id in countsfiles:
        c = Corpus.objects.get(id=corpus_id)
        n = max(countsfiles[corpus_id])
        corpus_path_prefix = os.path.join(CLUSTER_GUI_DIR, TREE_PATH, str(c.id), c.file_name)	
        count_file = corpus_path_prefix + ".M" + str(n) + ".cnt"
        counts.append(count_file)

    job_name = "combine_{0}".format(str(lm.id))
    qsub_call(COMBINE_SCRIPT, counts, job_name, job_names)
    job_names.append(job_name)

    temp = qsub_call(CREATE_ARPA_SCRIPT, [lm_prefix, lm_prefix, lm_prefix, str(lm.id)], None, job_names)
    # The next line is part of the ARPA script now.
    # remove_file(lm_cnt_path(lm))
    return temp

def run_perplexity(experiment):
    """
        Run a perplexity experiment using the given LM and corpus
        and save under the given experiment id
    """
    lm = experiment.lm

    lm_file = os.path.join(CLUSTER_GUI_DIR, LM_PATH, str(lm.id), file_name(lm.name))
    test_corpus = os.path.join(CLUSTER_BASE, experiment.corpus_location())
    directory = os.path.join(CLUSTER_GUI_DIR, EXP_PATH, str(experiment.experiment_set_id))
    output_location = os.path.join(directory, str(experiment.id) + ".txt")
    
    return qsub_call(PERPLEXITY_SCRIPT, [lm_file, lm_file, test_corpus, output_location, str(experiment.id)])

def qsub_call(script, args, name=None, wait_for=None):
    """
        Run a given qsub call and return the job id
        Parameters:
            script: the path to the script to execute
            args: an array of script arguments
            name: the name of the job (which can be later used to have other jobs wait for it to finish)
            wait_for: an array of jobs that need to finish before this job can be executed
    """
    
    call = '"qsub '
    if name:
        call += "-N {0} ".format(name)
    if wait_for:
        call += "-hold_jid {0} ".format(",".join(wait_for))
    call += script + " "
    call += " ".join(args)
    call += '"'
    
    subprocess.check_output(["ssh -C slund@cl5lx " + call], shell=True)
