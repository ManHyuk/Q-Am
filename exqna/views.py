# exqna/views.py
from django.shortcuts import render, redirect,get_object_or_404
from .models import ExtraQuestion, ExtraAnswer, Required
from .forms import ExtraAnswerForm, RequiredModelForm
from django.utils import timezone


def exquestion(request, user_id):
    #추가질문에 대해 대답하는 뷰
    exquestion = ExtraQuestion.objects.filter(is_new=True).first() #안 쓰인 것들 중 가장 오래된 것 exquestion
    if not exquestion: #안 쓰인 것 없을 경우
        return redirect('qna:main')

    has_extraAnswer = ExtraAnswer.objects.filter(user_id=user_id, question_id=exquestion.id)    #이미 질문했으면 넘어가기
    if has_extraAnswer:
        return redirect('qna:main')

    if request.method == 'POST':
        form = ExtraAnswerForm(request.POST)
        if form.is_valid():
            extraAnswer = form.save(commit=False)
            extraAnswer.user = request.user
            extraAnswer.question_id = exquestion.id
            extraAnswer.save()
            return redirect('qna:main')
    else:
        form = ExtraAnswerForm()

    return render(request, 'exqna/exquestion.html', {
            'exquestion': exquestion,
            'form': form,
        })

def required(request, user_id):
    #질문 요청하는 뷰
    if request.method == 'POST':
        form = RequiredModelForm(request.POST)
        already_required = Required.objects.filter(user_id=user_id, created_at__year=timezone.now().year, created_at__month=timezone.now().month, created_at__day=timezone.now().day)
        if already_required:    #하루에 질문 하나만 요청할 수 있게 만듦.
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

def exquestion_detail(request, ex_answer_id):
    ex_answer=get_object_or_404(ExtraAnswer,id=ex_answer_id)
    return render(request,'exqna:exquestion_detail.html')

def exquestion_edit(request, ex_answer_id):
    #추가 질문 수정하는 뷰
    extraAnswer=get_object_or_404(ExtraAnswer, id=answer_id)
    if extaAnswer.created_at.hour + 1 > timezone.now().hour:    #1시간 지났을 경우 수정 불가
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
    return render(request, 'qna/exquestion_edit.html', {
            'form':form,
            'answer':extraAnswer,
        })
