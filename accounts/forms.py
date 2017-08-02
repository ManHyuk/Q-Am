from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from accounts.models import Profile

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', )

    phone_number=forms.CharField()
    address=forms.CharField()
    nickname=forms.CharField()

    def save(self):
        user=super().save()
        Profile.objects.create(
            user=user,
            phone_number=self.cleaned_data['phone_number'],
            address=self.cleaned_data['address'],
            nickname=self.cleaned_data['nickname'],
            )
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname']




