# exqna/forms.py
from django import forms
from .models import ExtraAnswer, Required

class ExtraAnswerForm(forms.ModelForm):
    class Meta:
        model = ExtraAnswer
        fields = ['content', 'is_public']


class RequiredModelForm(forms.ModelForm):
    class Meta:
        model = Required
        fields = ['title', 'content']