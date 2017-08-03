from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as auth_login
from .forms import SignupForm,ProfileForm
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from accounts.models import Profile


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(settings.LOGIN_URL)  # default : '/accounts/login'
    else:
        form = SignupForm()

    return render(request, 'accounts/signup_form.html', {'form': form, })

@login_required
def signup_info(request):
    # 회원 가입 추가정보 받아오기
    if Profile.objects.filter(user=request.user).exists():
        # 프로필이 이미 있으면 질문페이지로
        return redirect('qna:question')

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            try:
                # 카카오가 있으면
                profile.user.username = profile.user.socialaccount_set.first().extra_data['properties']['nickname'] # 유저의 이름은 카카오톡 닉네임으로 저장
            except AttributeError:
                # 없어서 에러가 나면
                profile.user=request.user
            finally:
                profile.user.save()
                profile.save()

            return redirect('qna:question')
    else:
        form = ProfileForm

    return render(request, 'accounts/signup_info.html', {
        'form': form,
        })


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')



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
                      template_name='accounts/login_form.html',
                      extra_context={'providers': providers})
