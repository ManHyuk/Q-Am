from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings


urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup_info/$', views.signup_info, name='signup_info'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout', kwargs={'next_page': '/accounts/login'}), #로그아웃 시 홈페이지로 이동
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^edit_pw/$',views.edit_pw, name='edit_pw'),


    url(r'^reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
            views.reset_confirm, name='reset_confirm'),
    url(r'^reset/$', views.reset, name='reset'),
    ]

