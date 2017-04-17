""" ExperimentSetForm model for generating the Run Experiment form
"""

from django import forms
from corpora.models import Corpus
from lm.models import LM
from experiments.models import ExperimentSet
from django.template.defaultfilters import mark_safe
from django.forms.widgets import RadioSelect, SelectMultiple

INPUT_TEXT_PLACEHOLDER = "Enter some test text here."

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

class ExperimentSetForm(forms.ModelForm):
    """Create a form for an Experiment Set
    """
    
    lm = forms.MultipleChoiceField(label="Language Models", required=False)

    source = forms.ChoiceField(choices=[["corpus", "corpus"], ["input_text", "input_text"]],
                                  widget=RadioSelect())
    
    corpus = forms.MultipleChoiceField(label=_radio_button_label("source", "corpus", "Test Corpora", 0),
                                  widget=SelectMultiple(attrs={"disabled" : 'True'}), required=False)

    input_text = forms.CharField(widget=forms.Textarea(attrs={"placeholder" : INPUT_TEXT_PLACEHOLDER, 'rows': 6}),
            label= _radio_button_label("source", "input_text", 'Input Text', 1, True), required=False)

    def validate_nonempty_input(self, cleaned_data):
        if len(cleaned_data.get("input_text")) < 1:
            self.add_error("input_text","Please enter a non-empty input text.")

    def validate_lm(self, cleaned_data):
        lm_ids = cleaned_data.get("lm")
        # Validate that the LM IDs are correct
	if not lm_ids : self.add_error("lm", "Please select at least one trained LM.")
	else :
	    for lm_id in lm_ids :
                try:
                    selected_lm = LM.objects.get(id=lm_id)
                except LM.DoesNotExist:
                    self.add_error("lm", "A selected LM does not exist.")
	        finally :
	            if selected_lm.status != LM.TRAINED : self.add_error("lm", "A selected LM is not trained.")

    def validate_corpora(self, cleaned_data):
        corpus_ids = cleaned_data.get("corpus")
        # Validate that the Corpus are is correct
	if not corpus_ids : self.add_error("corpus", "Please select at least one test corpus.")
	else :
	    for corpus_id in corpus_ids :
                try:
                    selected_corpus = Corpus.objects.get(id=corpus_id)
                except Corpus.DoesNotExist:
                    self.add_error("corpus", "A selected corpus does not exist.")

    def clean(self):
        cleaned_data = super(ExperimentSetForm, self).clean()
        exp_type = cleaned_data.get("source")
        self.validate_lm(cleaned_data)
        if exp_type == "input_text" : self.validate_nonempty_input(cleaned_data)
        else : self.validate_corpora(cleaned_data)
        return cleaned_data
        
    
    def __init__(self, *args, **kwargs):
            super(ExperimentSetForm, self).__init__(*args,**kwargs)

            lm_choices     = [(l.id, l.name) for l in LM.objects.filter(status = LM.TRAINED)]
            corpus_choices = [(c.id, c.name) for c in Corpus.objects.all()]
            self.fields['lm'].choices = lm_choices
	    self.fields['corpus'].choices = corpus_choices
    
    class Meta:
        model = ExperimentSet
        fields = ['lm', 'source', 'corpus', 'input_text']

