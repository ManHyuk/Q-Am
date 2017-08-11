from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, AuthenticationForm, UsernameField
from django import forms
from accounts.models import Profile
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User
from imagekit.forms import ProcessedImageField


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Check Password'


class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['name','nickname','phone_number','email','img']

    def __init__(self,*args,**kwargs):
        super(ProfileForm,self).__init__(*args,**kwargs)
        self.fields['name'].widget.attrs['placeholder']='Name'
        self.fields['nickname'].widget.attrs['placeholder'] = 'Nickname(공유될 때 이름)'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'PhoneNumber/ex>01012341234'
        self.fields['email'].widget.attrs['placeholder'] = 'E-Mail/ex>qam@qam.qam'

        # fields=['name','nickname','phone_number','email','img']



    # name=forms.CharField(
    #         label='',
    #         max_length=254,
    #         widget=forms.TextInput(attrs={
    #             'autofocus': '',
    #             'placeholder': 'name'
    #         })
    #     )
    # nickname = forms.CharField(
    #     help_text='',
    #     label='',
    #     widget=forms.TextInput(attrs={
    #             'autofocus': '',
    #             'placeholder': 'nickname(공유될 때 이름)'
    #         }))
    # phone_number = forms.CharField(
    #     # help_text='ex> 01012341234',
    #     label='',
    #     widget=forms.TextInput(attrs={
    #             'autofocus': '',
    #             'placeholder': 'phone number/ex>01012341234'
    #         }))
    # email = forms.EmailField(
    #             max_length=100,
    #             label='',
    #             widget=forms.TextInput(attrs={
    #                              'autofocus': '',
    #                              'placeholder': 'email/ex>qam@qam.qam'
    #                          }))
    # # img = ProcessedImageField(spec_id='accounts:profile:img')



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

