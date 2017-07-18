from django.shortcuts import render, redirect
from .models import ExtraQuestion

def exquestion(request):
    exquestion = ExtraQuestion.objects.filter(is_new=True).first() #안 쓰인 것들 중 가장 오래된 것 exquestion
    if not exquestion: #안 쓰인 것 없을 경우
        return redirect('qna:main')

    return render(request, 'exqna/exquestion.html', {'exquestion': exquestion})
