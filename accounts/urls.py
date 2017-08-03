from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup-info/$', views.signup_info, name='signup_info'),
    url(r'^login/$', views.login, name='login'),
    # url(r'^login/$', auth_views.login, name='login', kwargs={'template_name': 'accounts/login_form.html'}),
    url(r'^logout/$', auth_views.logout, name='logout', kwargs={'next_page': '/accounts/login'}), #로그아웃 시 홈페이지로 이동
    url(r'^profile/$', views.profile, name='profile'),
]
