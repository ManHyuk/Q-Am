from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, AuthenticationForm, UsernameField
from django import forms
from accounts.models import Profile
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User
from imagekit.forms import ProcessedImageField

class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].placeholder="id"
        # if self._meta.model.USERNAME_FIELD in self.fields:
        #     self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    error_messages = {
        'password_mismatch': ("비밀번호가 일치하지 않습니다."),
    }
    password1 = forms.CharField(
        label=(""),
        strip=False,
        widget=
            forms.PasswordInput(),
            # forms.TextInput(attrs={'placeholder': '비밀번호'}),

    )
    password2 = forms.CharField(
        label=(""),
        widget=
            forms.PasswordInput(),
            # forms.TextInput(attrs={'placeholder': '비밀번호확인'}),

        strip=False,
        )




class ProfileForm(forms.Form):
    name=forms.CharField(
            label='',
            max_length=254,
            widget=forms.TextInput(attrs={
                'autofocus': '',
                'placeholder': 'name'
            })
        )
    nickname = forms.CharField(
        help_text='',
        label='',
        widget=forms.TextInput(attrs={
                'autofocus': '',
                'placeholder': 'nickname(공유될 때 이름)'
            }))
    phone_number = forms.CharField(
        # help_text='ex> 01012341234',
        label='',
        widget=forms.TextInput(attrs={
                'autofocus': '',
                'placeholder': 'phone number/ex>01012341234'
            }))
    email = forms.EmailField(
                max_length=100,
                label='',
                widget=forms.TextInput(attrs={
                                 'autofocus': '',
                                 'placeholder': 'email/ex>qam@qam.qam'
                             }))
    # img = ProcessedImageField(spec_id='accounts:profile:img')


    def save(self,commit=True):
        profile = Profile(**self.cleaned_data)
        if commit :
            profile.save()
        return profile





class EditPasswordForm(forms.Form):
    pw1 = forms.CharField(max_length=50, label="new password", widget=forms.PasswordInput)
    pw2 = forms.CharField(max_length=50, label="new password again", widget=forms.PasswordInput)




class LoginForm(AuthenticationForm):
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'autofocus': '',
            'placeholder': 'Username'
        }),
        label=''
    )
    password = forms.CharField(
        label=(""),
        strip=False,
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    error_messages = {
        'invalid_login': (
            "아이디와 비밀번호를 다시 확인해 주세요."
        ),
        'inactive': ("계정이 정지되었습니다."),
    }

