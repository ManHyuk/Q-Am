# exqna/views.py
from django.shortcuts import render, redirect
from .models import ExtraQuestion, ExtraAnswer, Required
from .forms import ExtraAnswerForm, RequiredModelForm
from django.utils import timezone


def exquestion(request, user_id):
    exquestion = ExtraQuestion.objects.filter(is_new=True).first() #안 쓰인 것들 중 가장 오래된 것 exquestion
    if not exquestion: #안 쓰인 것 없을 경우
        return redirect('qna:main')

    has_extraAnswer = ExtraAnswer.objects.filter(user_id=user_id, question_id=exquestion.id)
    if has_extraAnswer:
        return redirect('qna:main')

    if request.method == 'POST':
        form = ExtraAnswerForm(request.POST)
        if form.is_valid():
            extraAnswer = ExtraAnswer.objects.create(user_id=user_id, question_id=exquestion.id, content=form.cleaned_data['content'])
            return redirect(extraAnswer)
    else:
        form = ExtraAnswerForm()

    return render(request, 'exqna/exquestion.html', {
            'exquestion': exquestion,
            'form': form,
        })

def required(request, user_id):
    if request.method == 'POST':
        form = RequiredModelForm(request.POST)
        already_required = Required.objects.filter(user_id=user_id, created_at__year=timezone.now().year, created_at__month=timezone.now().month, created_at__day=timezone.now().day)
        if already_required:
            return render(request, 'exqna/already_required.html')
        if form.is_valid():
            required = form.save(commit=False)
            required.user_id = user_id
            required.save()
            return redirect(required)
    else:
        form = RequiredModelForm()

    return render(request, 'exqna/required.html', {
            'form': form,
        })
