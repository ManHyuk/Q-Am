from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from accounts.models import Profile

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname']

