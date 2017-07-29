from django.conf import settings
from django.db import connection
from django.template import Template, Context
from datetime import date
from django.shortcuts import redirect, render, get_object_or_404
from .models import Question
from qna.utils import get_today_id
import re

class QuestionMiddleware(object):

    DISALLOW_URLS = [
        r'^/accounts/profile/',
        r'^/qna/[0-9a-zA-Z]+',
        r'^/exqna/',
        r'^/diary/',
    ]

    def __init__(self, get_response):
        # 미들웨어 초기화 함수, get_response 외에 인자를 받을 수 없다.
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_request(self, request):
        return

    def process_view(self, request, view_func, view_args, view_kwargs):
        # 장고의 view가 호출되기 전에 실행된다.

        today_id = get_today_id()

        # if request.user.answer_set.filter(question_id=today_id).exists():
        #     # 오늘 질문에 대한 답이 있을 경우
        #     return None

        for pattern in self.DISALLOW_URLS:
            if re.match(pattern, request.path):
                return redirect('qna:question')

        return None

    def process_template_response(self, request, response):
        # 장고의 view가 실행이 끝난 후 실행된다.
        return response


    def process_response(self, request, response):
        return response



