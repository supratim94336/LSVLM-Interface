"""
    Utility functions for corpus file management
"""

from django.utils.text import slugify
import os, shutil, subprocess

CLUSTER_BASE = "/data/corpora/lsvlm"
WEBSERVER_BASE = "/data"

GUI_ACCOUNT_DIR = ""
CLUSTER_GUI_DIR = os.path.join(CLUSTER_BASE, GUI_ACCOUNT_DIR)
WEBSERVER_GUI_DIR = os.path.join(WEBSERVER_BASE, GUI_ACCOUNT_DIR)

TMP_PATH = "tmp"
UPLOAD_PATH = "uploads"
TREE_PATH = "trees"
LM_PATH = "lm"
SCRIPTS_PATH = "scripts"
EXP_PATH = "experiments"

INPUT_TEXT = 2

def corpus_path(corpus):
    """
        Get the full file path for the given corpus.
    """
    #return corpus.file_path()
    return os.path.join(WEBSERVER_BASE, corpus.file_path())

def valid_directory(path):
    """
        Check if the given directory path is valid.
    """
    full_path = os.path.join(WEBSERVER_BASE, path.strip("/"))
    #return os.path.isdir(path)
    return os.path.isdir(full_path)

def valid_path(path):
    """
        Check if the given file path leads to a valid file.
    """
    full_path = os.path.join(WEBSERVER_BASE, path.strip("/"))
    #return os.path.isfile(path)
    return os.path.isfile(full_path)
    
def open_path(path):
    """
        Returns a file pointer to the given corpus path.
    """
    full_path = os.path.join(WEBSERVER_BASE, path.strip("/"))
    #return open(path, "r")
    return open(full_path, "r")

def corpus_sample(path, num_lines):
    """
        Convenience function to the first num_lines lines from the corpus
        to display a preview.
    """
    f = open_path(path)
    lines = ""
    for n in range(num_lines):
        line = f.readline()
        lines += line[0:min(len(line), 500)]
    return lines
    f.close()

def file_size(path):
    """                                    
        Convenience function to the size of a file at path        
    """
    full_path = os.path.join(WEBSERVER_BASE, path.strip("/"))
    return str(os.path.getsize(full_path)) + " bytes"

def wc(path):
    """                                    
        Returns the number of lines, words, and chars in a file at path
    """
    full_path = os.path.join(WEBSERVER_BASE, path.strip("/"))
    counts = subprocess.check_output(['wc', full_path]).split()
    return counts[0] + " lines, " + counts[1] + " words, " + counts[2] + " characters"

def write_tmp_file(file, name):
    """
        Write a temporary file and then return the local path it is saved at.
    """
    name = file_name(name)
    path = os.path.join(WEBSERVER_GUI_DIR, TMP_PATH, name)
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return os.path.join(GUI_ACCOUNT_DIR, TMP_PATH, name)

def save_tmp_file(name):
    """
        Copy a temporary file to the upload directory to permanently save it.
    """
    name = file_name(name)
    tmp_path = os.path.join(WEBSERVER_GUI_DIR, TMP_PATH, name)
    upload_path = os.path.join(WEBSERVER_GUI_DIR, UPLOAD_PATH, name)
    shutil.move(tmp_path, upload_path)
    return (os.path.join(GUI_ACCOUNT_DIR, UPLOAD_PATH), name)

def file_name(name):
    """
        Change the given corpus name into a suitable ASCII file name
    """
    return slugify(name) + ".txt"
    #return name + ".txt"

def file_contents(path):
    f = open(path)
    content = f.read()
    f.close()
    return content

def remove_file(path):
    try:
        os.remove(path)
    except:
        pass

def remove_empty_folder(path):
    try:
        os.rmdir(path)
    except:
        pass

def write_lm_file(lm_name, lm_id, text):
    
    f = open(os.path.join(WEBSERVER_GUI_DIR, LM_PATH, str(lm_id), file_name(lm_name) + ".lm"), 'w')
    f.write(text.encode('utf8'))
    f.close()
    return os.path.join(GUI_ACCOUNT_DIR, LM_PATH, str(lm_id), file_name(lm_name))

def arpa_file_path(lm):
    """
        Get the content of the arpa file on the webserver (for downloading)
    """
    return os.path.join(WEBSERVER_GUI_DIR, LM_PATH, str(lm.id), file_name(lm.name) + ".arpa")

def lm_file_path(lm):
    """
        Get the path of the lm file on the webserver (for downloading)
    """
    return os.path.join(WEBSERVER_GUI_DIR, LM_PATH, str(lm.id), file_name(lm.name) + ".lm")

def lm_voc_path(lm):

    """
        Get the path of the lm file on the webserver (for downloading)
    """
    return os.path.join(WEBSERVER_GUI_DIR, LM_PATH, str(lm.id), file_name(lm.name) + ".voc")

def lm_cnt_path(lm):

    """
        Get the path of the lm file on the webserver (for downloading)
    """
    return os.path.join(WEBSERVER_GUI_DIR, LM_PATH, str(lm.id), file_name(lm.name) + ".cnt")

def remove_lm_files(lm):
    remove_file(arpa_file_path(lm))
    remove_file(lm_file_path(lm))
    remove_file(lm_voc_path(lm))
    remove_empty_folder(os.path.join(WEBSERVER_GUI_DIR, LM_PATH, str(lm.id)))
    return None

def remove_exp_set_files(exp_set):
    if exp_set.experiment_type == INPUT_TEXT : remove_file(experiment_corpus_file_path(exp_set))
    for experiment in exp_set.experiment_set.all() :
        remove_file(experiment_results_file_path(experiment))
    remove_empty_folder(os.path.join(WEBSERVER_GUI_DIR, EXP_PATH, str(exp_set.id)))
    return None

def count_file_path(count_file):
    """
        Get the path of the count file on the webserver (for downloading)
    """
    return os.path.join(WEBSERVER_GUI_DIR, TREE_PATH, str(count_file.corpus.id), count_file.file_name())

def make_lm_dir(lm_id):
    """
        Get the path of the experiment file on the webserver (for downloading)
    """
    directory = os.path.join(WEBSERVER_GUI_DIR, LM_PATH, str(lm_id))
    subprocess.call(["mkdir -m 777 " + directory], shell=True)
    return None

def make_experiment_dir(exp_set_id):
    """
        Get the path of the experiment file on the webserver (for downloading)
    """
    directory = os.path.join(WEBSERVER_GUI_DIR, EXP_PATH, str(exp_set_id))
    subprocess.call(["mkdir -m 777 " + directory], shell=True)
    return None

def experiment_corpus_file_path(experiment_set):
    """
        Get the path of the experiment file on the webserver (for downloading)
    """
    return os.path.join(WEBSERVER_GUI_DIR, EXP_PATH, str(experiment_set.id), str(experiment_set.id) + "_corpus.txt")

def experiment_results_file_path(experiment):
    """
        Get the path of the experiment file on the webserver (for downloading)
    """
    return os.path.join(WEBSERVER_GUI_DIR, EXP_PATH, str(experiment.experiment_set_id), str(experiment.id) + ".txt")

def write_experiment_corpus(exp_set_id, text):
    file_name = str(exp_set_id) + "_corpus.txt"
    f = open(os.path.join(WEBSERVER_GUI_DIR, EXP_PATH, str(exp_set_id), file_name), 'w')
    f.write(text.encode('utf8'))
    f.close()
    return os.path.join(GUI_ACCOUNT_DIR, EXP_PATH, str(exp_set_id), file_name)

def tail( path, lines=20 ):
    f = open(path)
    total_lines_wanted = lines

    BLOCK_SIZE = 1024
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = [] # blocks of size BLOCK_SIZE, in reverse order starting
                # from the end of the file
    while lines_to_go > 0 and block_end_byte > 0:
        if (block_end_byte - BLOCK_SIZE > 0):
            # read the last block we haven't yet read
            f.seek(block_number*BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            # file too small, start from begining
            f.seek(0,0)
            # only read what was not read
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count('\n')
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = ''.join(reversed(blocks))
    f.close()
    return '\n'.join(all_read_text.splitlines()[-total_lines_wanted:])
