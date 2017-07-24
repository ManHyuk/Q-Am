# qna/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question, Answer
# import time
from .forms import AnswerForm
from django.utils import timezone
from django.db.models import Q
from exqna.models import ExtraQuestion, ExtraAnswer


def question(request, user_id):
    days = '1'
    # days에 걸리는 함수를 통해 오늘이 365일 중에 몇 번째 날인지 파악
    now = int(days)
    ques = Question.objects.get(id=now)
    # 그날에 맞는 질문을 골라 온다.
    already_answer = Answer.objects.filter(question_id=now, created_at__year=timezone.now().year)  # 오늘 이미 답변했으면 넘어가기
    if already_answer:
        redirect('exqna:exquestion', user_id=user_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = ques
            answer = form.save()
            return redirect('qna:main')
    else:
        form = AnswerForm()
    return render(request, 'qna/question.html', {

        'form': form,
        'question': ques,
    })


def main(request):
    return render(request, 'qna/main.html')


def question_search(request):
    if request.GET.get('search'):
        search = request.GET.get('search')
        search_ques1 = Answer.objects.all()
        search_ques1 = search_ques1.filter(Q(question__question__icontains=search) | Q(content__icontains=search))
        search_ques2 = ExtraAnswer.objects.all()
        search_ques2 = search_ques2.filter(Q(question__title__icontains=search) | Q(content__icontains=search))
        return render(request, 'qna/question_search.html', {
            'search': search,
            'search_ques1': search_ques1,
            'search_ques2': search_ques2,
        })
    else:
        return render(request, 'qna/question_search.html')


def question_detail(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    return render(request, 'qna/question_detail.html', {
        'answer': answer,
    })


def question_edit(request, answer_id):
    days = '1'
    # days에 걸리는 함수를 통해 오늘이 365일 중에 몇 번째 날인지 파악
    now = int(days)
    ques = Question.objects.get(id=now)
    # 그날에 맞는 질문을 골라 온다.
    answer = get_object_or_404(Answer, id=answer_id)
    if answer.created_at.hour + 1 > timezone.now().hour:  # 1시간 지났을 경우 수정 불가
        return redirect('qna:main')
    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES, instance=answer)
        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.user = request.user
            new_answer.question = ques
            new_answer.save()
            return redirect('qna:main')
    else:
        form = AnswerForm(instance=answer)
    return render(request, 'qna/question_detail.html', {
        'form': form,
        'question': ques,
    })
