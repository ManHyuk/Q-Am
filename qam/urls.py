"""qam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url

from django.contrib import admin
from django.shortcuts import redirect, render


urlpatterns = [
    url(r'^$', lambda request: render(request, 'base.html'), name='root'), # TODO test용 삭제할것

    url(r'^admin/', admin.site.urls),
    url(r'^qna/', include('qna.urls', namespace='qna')),
    url(r'^exqna/', include('exqna.urls', namespace='exqna')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^diary/', include('diary.urls', namespace='diary')),


]

