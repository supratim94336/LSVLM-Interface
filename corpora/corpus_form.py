""" CorpusForm model for generating the Add Corpus form
"""

from django import forms
from corpora.models import Corpus, Lang
from django.template.defaultfilters import mark_safe
from django.core.validators import URLValidator
from django.forms.widgets import RadioSelect
from util import files
import os

DESCRIPTION_PLACEHOLDER = """Please enter a description of the corpus, \
including information such as the source of the data, date, genre, number \
of sentences, etc.
"""

PROCESS_STEPS_PLACEHOLDER = """Please enter any processing steps done to \
the corpus before uploading, such as tokenization, normalization of numbers, etc.
"""

def _radio_button_label(name, value, label_text, radio_number, checked = False):
    """Create a label for a form field with a radio button next to it

    Parameters:
        name - the name of the entire radio field
        value - the value of the particular radio button
        label_text - the text to display next to the button
        checked - True if the radio button is selected (default False)
    """
    
    if checked:
        checked = 'checked="checked"'
    else:
        checked = ""
    template = '<input type="radio" name="{0}" value="{1}" id="id_{0}_{4}" {2}/> {3}'
    return mark_safe(template.format(name, value, checked, label_text, radio_number))

class CorpusForm(forms.ModelForm):
    """Create a form for a Corpus object
    """
    
    name = forms.CharField(label="Name", max_length=200, widget=forms.TextInput(attrs={"placeholder" : "Name"}))
    description = forms.CharField(widget=forms.Textarea(attrs=
        {"placeholder": DESCRIPTION_PLACEHOLDER, 'rows': 4}), label="Description", required=False)
    process_steps = forms.CharField(widget=forms.Textarea(attrs=
        {"placeholder" : PROCESS_STEPS_PLACEHOLDER, 'rows' : 4}), label="Processing Steps", required=False)
    
    
    lang_select = forms.ChoiceField(label="Language")
    
    new_lang = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Language Name"}), label="Language Name",
                required=False)
    
    metadata_url = forms.CharField(label="Metadata URL", widget=forms.TextInput(attrs=
            {"placeholder" : "http://www.example.com/corpus_info.html"}),
            validators=[URLValidator], required=False)
    
    path_type = forms.ChoiceField(choices=[["file_path", "file_path"], ["file_upload", "file_upload"]],
                                  widget=RadioSelect())
    
    location = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "/path/to/corpus"}),
            label= _radio_button_label("path_type", "file_path", 'Corpus Location', 0, True), required=False)
    
    file_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "corpus.txt" }),
            label="Corpus File Name", required=False)

    label = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "enter project properties (space separated)" }),
            label="Labels", required=False)
            
    upload_path = forms.FileField(label=_radio_button_label("path_type", "file_upload", "Upload File", 1),
                                  widget=forms.ClearableFileInput(attrs={"disabled" : 'True'}), required=False)
                                  
    # A check has been added for mandatorily adding data in either description or metadata_url field
    def validate_min_metadata(self, cleaned_data):
        description = cleaned_data.get("description")
        metadata_url = cleaned_data.get("metadata_url")
        if len(description) < 1:
            if len(metadata_url) < 1:
                self.add_error("metadata_url","Enter either description or metadata_url")
                self.add_error("description","Enter either description or metadata_url")




    def validate_lang(self, cleaned_data):
        lang_id = cleaned_data.get("lang_select")
        
        # Validate that the language ID or new language is correct
        if(lang_id == "new"):
            new_lang_name = cleaned_data.get("new_lang")
            if len(new_lang_name) < 1:
                self.add_error("new_lang", "Please enter a language name.")
            elif Lang.objects.filter(name=new_lang_name).exists():
                self.add_error("new_lang", "Language name is already in use.")
        else:
            try:
                lang = Lang.objects.get(id=lang_id)
            except Lang.DoesNotExist:
                self.add_error("lang_id", "Language does not exist.")
    
    def validate_location(self, cleaned_data):
        # Validate that the given file location is correct
        file_type = cleaned_data.get("path_type")
        if(file_type == "file_path"):
            location = cleaned_data.get("location").strip("/")
            file_name = cleaned_data.get("file_name").strip("/")
            if not files.valid_directory(location):
                self.add_error("location", "Invalid file location.")
            elif not files.valid_path(os.path.join(location, file_name)):
                self.add_error("file_name", "Invalid file path.")
        elif (file_type == "file_upload"):
            upload_path = cleaned_data.get("upload_path")
            if not upload_path:
                self.add_error("upload_path", "Please select a file.")
        else: 
            # We shouldn't get here, but just in case
            self.add_error("file_name", "Invalid file path.")
        
    
    def clean(self):
        cleaned_data = super(CorpusForm, self).clean()
        self.validate_min_metadata(cleaned_data) # calling newly added function
        self.validate_lang(cleaned_data)
        self.validate_location(cleaned_data)
        
        return cleaned_data
        
    
    def __init__(self, *args, **kwargs):
            super(CorpusForm, self).__init__(*args,**kwargs)

            lang_choices = [(l.id, l.name) for l in Lang.objects.all()]
            lang_choices.append(('new', "-- Add New Language --"))
            self.fields['lang_select'].choices = lang_choices
    
    class Meta:
        model = Corpus
        fields = ['name', 'description', 'process_steps', 'lang_select', 'new_lang',
            'metadata_url', 'location', 'file_name', 'upload_path']


# Form for editing an existing corpus (can change all fields but corpus location)
class CorpusEditForm(CorpusForm):
    
    file_name = None
    path_type = None
    location = None
    upload_path = None
    
    def clean(self):
        cleaned_data = super(CorpusForm, self).clean()
        
        self.validate_lang(cleaned_data)
        
        return cleaned_data

    def __init__(self, *args, **kwargs):
            super(CorpusEditForm, self).__init__(*args,**kwargs)
            self.initial["lang_select"] = self.instance.lang.id

    #Label field has been added in class Meta to reflect changes of field value while editing
    class Meta:
        model = Corpus
        fields = ['name', 'description', 'process_steps', 'lang_select', 'new_lang', 'metadata_url', 'label']