from email.policy import default
from django import forms

class QuestionForm(forms.Form):
    question = forms.CharField(max_length=200,widget=forms.Textarea)

class OptionForm(forms.Form):
    text = forms.CharField(max_length=100,widget=forms.Textarea)
    is_true = forms.BooleanField(default=False)    
