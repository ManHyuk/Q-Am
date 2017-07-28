from django.conf import settings
from django.db import connection
from django.template import Template, Context
from datetime import date
from django.shortcuts import redirect, render, get_object_or_404
from .models import Question
import re

class QuestionMiddleware(object):

    DISALLOW_URLS = [
        r'^/accounts/profile/',
        r'^/qna/[0-9a-zA-Z]+',
        r'^/exqna/',
        r'^/diary/',
    ]

    def __init__(self, get_response):
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
        print(request.path)

        today_id = Question.get_today_id()
        today_question = get_object_or_404(Question, id=today_id)

        if not request.user.is_anonymous():
            if request.user.answer_set.all():
                if request.user.answer_set.all().last().question == today_question:
                    return None

        for pattern in self.DISALLOW_URLS:
            if re.match(pattern, request.path):
                return redirect('qna:question')

        return None

    def process_template_response(self, request, response):
        return response


    def process_response(self, request, response):
        return response



