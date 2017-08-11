# exqna/views.py
from django.shortcuts import render, redirect,get_object_or_404
from .models import ExtraQuestion, ExtraAnswer, Required
from .forms import ExtraAnswerForm, RequiredModelForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from pytz import timezone as timezone_kor
import datetime
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



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
            extraanswer = form.save(commit=False)
            extraanswer.user = request.user
            extraanswer.question = exquestion
            extraanswer.save()
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
    already_required = Required.objects.filter(user=request.user,created_at__year=datetime.datetime.now(timezone_kor('Asia/Seoul')).year,created_at__month=datetime.datetime.now(timezone_kor('Asia/Seoul')).month,created_at__day=datetime.datetime.now(timezone_kor('Asia/Seoul')).day)
    # pytz를 이용하여 한국시간으로 timezone을 사용할 수 있었다
    # settings.py에서 한국 시간으로 변경하여 created_at시간도 다 한국시간이 됨
    # 고로 한국시간으로 매일매일 질문을 요청할 수 있게 됨
    if already_required:  # 하루에 질문 하나만 요청할 수 있게 만듦.
        today = datetime.datetime.now().day
        today = int(today)
        future = datetime.datetime.now().replace(hour=0, minute=0, second=0)+datetime.timedelta(days=1)
        return render(request, 'exqna/already_required.html',{
            'future':future,
        })
        # 메세지 만들어지면 required.html 로 넘어가자

    if request.method == 'POST':
        form = RequiredModelForm(request.POST)
        if form.is_valid():
            required = form.save(commit=False)
            required.user = request.user
            required.save()
            return redirect("qna:main")
    else:
        form = RequiredModelForm()

    return render(request, 'exqna/required.html', {
            'form': form,
        })


@login_required
def exquestion_detail(request, ex_answer_id):
    ex_answer=get_object_or_404(ExtraAnswer, id=ex_answer_id)
    if ex_answer.user_id != request.user.id:
        return redirect('qna:main')
    # url로 남의 답변에 접근 방지
    return render(request, 'exqna/exquestion_detail.html', {
            'ex_answer':ex_answer,
        })


@login_required
def exquestion_edit(request, ex_answer_id):
    #추가 질문 수정하는 뷰
    extraAnswer=get_object_or_404(ExtraAnswer, id=ex_answer_id)

    if extraAnswer.user_id != request.user.id:
        return redirect('qna:main')
    #url로 남의 답변에 접근 방지
    if extraAnswer.created_at + datetime.timedelta(hours=1) < timezone.now():
        messages.info(request, '수정 가능 시간이 지났습니다.')
        #1시간 지났을 경우 수정 불가
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


    #if로 바꿔서 오늘 추가질문이 없을 경우에 qna/other people 뷰로 넘어갈 수 있게
    if not exquestion:
        return redirect("qna:other_people")
    answer_set = ExtraAnswer.objects.filter(question=exquestion, is_public=True)   #공유한다고 한 것만 불러오기
    other_answer_set = answer_set.exclude(user=request.user)    #자기 답은 제외

    page = request.GET.get('page', 1)
    paginator = Paginator(other_answer_set, 12)

    try:
        other_answer = paginator.page(page)
    except PageNotAnInteger:
        other_answer = paginator.page(1)
    except EmptyPage:
        other_answer = paginator.page(paginator.num_pages)

    return render(request, 'exqna/other_people.html', {
            'exquestion':exquestion,
            'answer_set':other_answer_set,
            'other_answer': other_answer
        })