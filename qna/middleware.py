from django.conf import settings
from django.db import connection
from django.template import Template, Context
from datetime import date
from django.shortcuts import redirect, render

class QuestionMiddleware(object):
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
        allow_url = [
            '/qna',
            '/accounts/profile/',
        ]

        # if not request.user.is_anonymous():
        #     if request.user.answer_set.all().exists():
        #         if request.user.answer_set.all().first().created_at.day != date.today().day:
        #             if request.path not in  allow_url:
        #                 return redirect('qna:question')

    def process_template_response(self, request, response):
        return response


    def process_response(self, request, response):
        return response



