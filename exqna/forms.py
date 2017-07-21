# exqna/forms.py
from django import forms
from .models import ExtraAnswer, Required

class ExtraAnswerForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


class RequiredModelForm(forms.ModelForm):
    class Meta:
        model = Required
        fields = ['title', 'content']