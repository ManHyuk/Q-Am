# exqna/views.py
from django.shortcuts import render, redirect,get_object_or_404
from .models import ExtraQuestion, ExtraAnswer, Required
from .forms import ExtraAnswerForm, RequiredModelForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime


@login_required
def exquestion(request):
    #추가질문에 대해 대답하는 뷰
    exquestion = ExtraQuestion.objects.filter(is_new=True).first() #안 쓰인 것들 중 가장 오래된 것 exquestion
    if not exquestion: #안 쓰인 것 없을 경우
        return redirect('qna:main')

    has_extraAnswer = ExtraAnswer.objects.filter(question=exquestion, user=request.user)    #이미 대답했으면 넘어가기
    if has_extraAnswer:
        return redirect('qna:main')

    if request.method == 'POST':
        form = ExtraAnswerForm(request.POST)
        if form.is_valid():
            extraAnswer = form.save(commit=False)
            extraAnswer.user = request.user
            extraAnswer.question = exquestion
            extraAnswer.save()
            return redirect('qna:main')
    else:
        form = ExtraAnswerForm()

    return render(request, 'exqna/exquestion.html', {
            'exquestion': exquestion,
            'form': form,
        })

@login_required
def required(request):
    #질문 요청하는 뷰
    if request.method == 'POST':
        form = RequiredModelForm(request.POST)
        already_required = Required.objects.filter(user=request.user, created_at__year=timezone.now().year, created_at__month=timezone.now().month, created_at__day=timezone.now().day)
        if already_required:    #하루에 질문 하나만 요청할 수 있게 만듦.
            messages.warning(request, '질문은 하루에 하나만 요청할 수 있습니다.')    #그때 질문 요청했을 시 메세지 띄우기
            return render(request, 'exqna/already_required.html')   #메세지 만들어지면 required.html 로 넘어가자
        if form.is_valid():
            required = form.save(commit=False)
            required.user = request.user
            required.save()
            return redirect(required)
    else:
        form = RequiredModelForm()

    return render(request, 'exqna/required.html', {
            'form': form,
        })


@login_required
def exquestion_detail(request, ex_answer_id):
    ex_answer=get_object_or_404(ExtraAnswer, id=ex_answer_id)
    return render(request, 'exqna/exquestion_detail.html', {
            'ex_answer':ex_answer,
        })


@login_required
def exquestion_edit(request, ex_answer_id):
    #추가 질문 수정하는 뷰
    extraAnswer=get_object_or_404(ExtraAnswer, id=ex_answer_id)
    if extraAnswer.created_at + datetime.timedelta(hours=1) < timezone.now():    #1시간 지났을 경우 수정 불가
        return redirect('qna:main')
    if request.method=='POST':
        form=ExtraAnswerForm(request.POST, instance=extraAnswer)
        if form.is_valid():
            new_extraAnswer = form.save(commit=False)
            new_extraAnswer.user = request.user
            new_extraAnswer.question = extraAnswer.question
            new_extraAnswer.save()
            return redirect('qna:main')
    else :
        form = ExtraAnswerForm(instance=extraAnswer)
    return render(request, 'exqna/exquestion.html', {
            'form':form,
            'exquestion':extraAnswer.question,
        })


@login_required
def other_people(request):
    exquestion = ExtraQuestion.objects.filter(is_new=True).first()  #오늘의 추가질문 가져오기
    answer_set = ExtraAnswer.objects.filter(question=exquestion, is_public=True)   #공유한다고 한 것만 불러오기
    other_answer_set = answer_set.exclude(user=request.user)    #자기 답은 제외
    return render(request, 'exqna/other_people.html', {
            'exquestion':exquestion,
            'answer_set':other_answer_set,
        })
