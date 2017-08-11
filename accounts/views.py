from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as auth_login
from .forms import SignupForm, ProfileForm, EditPasswordForm, LoginForm
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from accounts.models import Profile
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.contrib.auth import get_user_model
from django.contrib import messages
from accounts.models import Profile
from qna.models import Answer
from exqna.models import ExtraAnswer


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            return redirect(settings.LOGIN_URL)  # default : '/accounts/login'
    else:
        form = SignupForm()

    return render(request, 'accounts/signup_form.html', {'form': form, })



@login_required
def signup_info(request):
    #회원 가입 추가정보 받아오기
    if Profile.objects.filter(user=request.user).exists():
        # 프로필이 이미 있으면 질문페이지로
        return redirect('qna:main')
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            return redirect('qna:question')
    else:
        form = ProfileForm

    return render(request, 'accounts/signup_info.html', {
        'form': form,
        })



@login_required
def profile(request):
    answer = Answer.objects.filter(user_id=request.user)
    answer_public = Answer.objects.filter(user_id=request.user,is_public=True).count()
    ex_answer = ExtraAnswer.objects.filter(user_id=request.user)
    ex_answer_public = ExtraAnswer.objects.filter(user_id=request.user, is_public=True).count()
    ctx = {
        'answer': answer,
        'answer_public': answer_public,
        'ex_answer': ex_answer,
        'ex_answer_public': ex_answer_public,
    }
    return render(request, 'accounts/profile.html', ctx)



def login(request):
    providers = []
    for provider in get_providers():

        # social_app속성은 provider에는 없는 속성입니다.
        try:
            provider.social_app = SocialApp.objects.get(provider=provider.id, sites=settings.SITE_ID)

        except SocialApp.DoesNotExist:
            provider.social_app = None
        providers.append(provider)



    return auth_login(request,
                      authentication_form=LoginForm,
                      template_name='accounts/login_form.html',
                      extra_context={'providers': providers})


@login_required
def edit_pw(request):
    user = get_user_model()
    user = user.objects.get(username=request.user)


    if request.method == 'POST':
        pw1 = request.POST.get('pw1')
        pw2 = request.POST.get('pw2')
        if pw1 != pw2 :
            messages.info(request, '새로운 비밀번호 두개가 일치하지 않습니다.')
            return redirect('edit_pw')
        else:
            user.set_password(pw1)
            user.save()
        return redirect('login')
    else:
        form = EditPasswordForm

        return render(request, 'accounts/edit_pw.html', {
            'form': form
        })




