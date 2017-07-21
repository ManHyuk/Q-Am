from django.shortcuts import render
from .models import ExtraQuestion

def question(request):
    question = ExtraQuestion.objects.first()
    return render(request, 'exqna/question.html', {'question': question})
