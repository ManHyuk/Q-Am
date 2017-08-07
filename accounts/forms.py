from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, AuthenticationForm, UsernameField
from django import forms
from accounts.models import Profile


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields


class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['name','nickname','phone_number','email','img']


class EditPasswordForm(forms.Form):
    pw1 = forms.CharField(max_length=50, label="new password", widget=forms.PasswordInput)
    pw2 = forms.CharField(max_length=50, label="new password again", widget=forms.PasswordInput)

class LoginForm(AuthenticationForm):
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'autofocus': '',
            'placeholder': 'id'
        }),
        label=''
    )
    password = forms.CharField(
        label=(""),
        strip=False,
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder':'password'}))