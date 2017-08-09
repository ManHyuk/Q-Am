# qna/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from .forms import AnswerForm
from exqna.forms import ExtraAnswerForm
from django.utils import timezone
from exqna.models import ExtraQuestion, ExtraAnswer
from django.contrib.auth.decorators import login_required
from qna.utils import get_today_id
import datetime
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



@login_required
def question(request):
    today_id = get_today_id()
    #우리가 윤년을 기본으로 하고 윤년이 아닌 년은 2월 29일 질문을 배제시키는 구조이기 때문에 이렇게 했다
    #today_id 기반이라 새벽 4시에 같이 바뀜

    question = Question.objects.get(id=today_id)
    # 그날에 맞는 질문을 골라 온다.
    already_answer = Answer.objects.filter(question=question, user=request.user, created_at__year=timezone.now().year)  # 오늘 이미 답변했으면 넘어가기

    if already_answer:
        return redirect('exqna:exquestion')

    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer = form.save()
            return redirect('exqna:exquestion')
    else:
        form = AnswerForm()


    # if 'check' in form.is_public:
    #     checked = 'asdnjkgsd'
    return render(request, 'qna/question.html', {
        'form': form,
        'question': question,
    })




@login_required
def main(request):
    today_id = get_today_id()
    question = Question.objects.get(id=today_id)  #오늘의 질문 불러오기
    qs = Answer.objects.filter(question=question, user=request.user)    #오늘의 질문에 대해 했던 답 싹 다 불러오기
    exquestion = ExtraQuestion.objects.filter(is_new=True).first()  #오늘의 추가질문 불러오기(없을 수도 있음)
    if not exquestion:
        return render(request, 'qna/main.html', {
            'question':question,
            'answer_list':qs,
        })
    has_extraAnswer = ExtraAnswer.objects.filter(question=exquestion, user=request.user).first()
    if has_extraAnswer:     #이미 대답했을 경우 추가질문의 대답도 보여주기
        return render(request, 'qna/main.html', {
            'question':question,
            'answer_list':qs,
            'exquestion':exquestion,
            'ex_answer':has_extraAnswer,
        })
    else:       #추가질문 대답안했을 경우 폼 만들어주기
        if request.method =='POST':
            form = ExtraAnswerForm(request.POST, request.FILES)
            if form.is_valid():
                extra_answer = form.save(commit=False)
                extra_answer.user = request.user
                extra_answer.question = exquestion
                extra_answer.save()
                return redirect('qna:main')
        else:
            form = AnswerForm()
    return render(request, 'qna/main.html', {
            'question':question,
            'answer_list':qs,
            'exquestion':exquestion,
            'form':form,
        })

#제목으로 검색
@login_required
def question_search(request):

    if request.GET.get('search_keyword'):  #이거 search 에서 search_keyword로 바꿈/ day검색과의 차별성을 위해
        today_id = get_today_id()
        search_keyword = request.GET.get('search_keyword')
        search_ques1 = Question.objects.exclude(answer=None)    #답 안한 것들 제거
        search_ques1 = search_ques1.filter(question__icontains=search_keyword, answer__user=request.user)  #질문에 search 들어있는 것만 선택
        search_ques2 = ExtraAnswer.objects.filter(question__title__icontains=search_keyword,user=request.user)    #추가질문 답한 것에 대해서도 질문에 search들어있는 것 선택

        for i in range(1, 11):  # 앞으로의 열흘 동안의 질문은 검색되지 않도록 하기
            exclude_id = (today_id + i) % 366  # 366을 넘는 경우에 대해서 나머지로 처리
        if not id:  # today_id+1이 0일 경우 366으로 바꿔줘야 함
                exclude_id = 366

        exclude_question = Question.objects.get(id=exclude_id)
        search_ques1 = search_ques1.exclude(question=exclude_question)
        search_ques1 = search_ques1.distinct()

        if search_ques1.count()==0 and search_ques2.count()==0 :
            messages.info(request, '검색결과가 없습니다')
            return redirect('qna:question_search')

    # 중복 제거
        return render(request, 'qna/question_search.html', {
        'search_keyword': search_keyword,
        'search_ques1': search_ques1,
        'search_ques2': search_ques2,
    })
    else:
        return render(request, 'qna/question_search.html')

#날짜로 검색
@login_required
def question_search_day(request):
    if request.GET.get('search_day'):
        today_id = get_today_id()
        search_day=request.GET.get('search_day')
        #search_day는 'July 26' 구조로 들어옴
        daylist = search_day.split(' ')

        def month_string_to_number(string):
            m = {
                'jan': 1,
                'feb': 2,
                'mar': 3,
                'apr': 4,
                'may': 5,
                'jun': 6,
                'jul': 7,
                'aug': 8,
                'sep': 9,
                'oct': 10,
                'nov': 11,
                'dec': 12
            }
            s = string.strip()[:3].lower()

            try:
                out = m[s]
                return out
            except:
                raise ValueError('Not a month')

        num=month_string_to_number(daylist[0])
        num=str(num)

        if daylist[1] < '10':
            daylist[1] = daylist[1][1]

        search_day_ques1=Question.objects.filter(month=num, day=daylist[1],  answer__user=request.user)

        search_day_ques2=ExtraAnswer.objects.filter(created_at__month=num,created_at__day=daylist[1],user=request.user)

        for i in range(1, 11):  # 앞으로의 열흘 동안의 질문은 검색되지 않도록 하기
            exclude_id = (today_id + i) % 366  # 366을 넘는 경우에 대해서 나머지로 처리
        if not id:  # today_id+1이 0일 경우 366으로 바꿔줘야 함
            exclude_id = 366

        exclude_question = Question.objects.get(id=exclude_id)
        search_day_ques1 = search_day_ques1.exclude(question=exclude_question)
        search_day_ques1 = search_day_ques1.distinct()

        if search_day_ques1.count()==0 and search_day_ques2.count()==0 :
            messages.info(request, '검색결과가 없습니다')
            return redirect('qna:question_search_day')

    # 중복 제거
        return render(request, 'qna/question_search_day.html', {
        'search_day': search_day,
        'search_ques1': search_day_ques1,
        'search_ques2':search_day_ques2,
    })

    else:
        return render(request, 'qna/question_search_day.html')

#내용으로 검색
@login_required
def question_search_content(request):
    if request.GET.get('search_content'):
        today_id = get_today_id()
        search_content=request.GET.get('search_content')

        search_content_ques1=Question.objects.filter(answer__content__icontains=search_content ,answer__user=request.user)

        search_content_ques2=ExtraAnswer.objects.filter(content__icontains=search_content ,user=request.user)

        for i in range(1, 11):  # 앞으로의 열흘 동안의 질문은 검색되지 않도록 하기
            exclude_id = (today_id + i) % 366  # 366을 넘는 경우에 대해서 나머지로 처리
        if not id:  # today_id+1이 0일 경우 366으로 바꿔줘야 함
            exclude_id = 366

        exclude_question = Question.objects.get(id=exclude_id)
        search_content_ques1 = search_content_ques1.exclude(question=exclude_question)
        search_content_ques1 = search_content_ques1.distinct()

        if search_content_ques1.count()==0 and search_content_ques2.count()==0 :
            messages.info(request, '검색결과가 없습니다')
            return redirect('qna:question_search_content')

        return render(request, 'qna/question_search_content.html',{
            'search_content':search_content,
            'search_content_ques1':search_content_ques1,
            'search_content_ques2':search_content_ques2,
        })
    else:
        return render(request, 'qna/question_search_content.html')



@login_required
def question_detail(request, question_id):
    answer_set = Answer.objects.filter(question__id=question_id, user=request.user)

    return render(request, 'qna/question_detail.html', {
        'answer_set': answer_set,
    })


@login_required
def question_edit(request, answer_id):
    today_id = get_today_id()
    question = Question.objects.get(id=today_id)  #오늘의 질문 불러오기
    answer = get_object_or_404(Answer, id=answer_id)

    if answer.user_id != request.user.id:
        return redirect('qna:main')
    # url로 남의 답변에 접근 방지
    if answer.created_at + datetime.timedelta(hours=1) < timezone.now():
        messages.info(request, '수정 가능 시간이 지났습니다.')
        # 1시간 지났을 경우 수정 불가

        return redirect('qna:main')

    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES, instance=answer)
        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.user = request.user
            new_answer.question = question
            new_answer.save()
            return redirect('qna:main')
    else:
        form = AnswerForm(instance=answer)

    return render(request, 'qna/question.html', {
        'form':form,
        'question' : question,
        })


@login_required
def other_people(request):
    today_id = get_today_id()
    question = Question.objects.get(id=today_id)    #오늘의 질문 불러오기
    answer_set = Answer.objects.filter(question=question, is_public=True)   #공유한다고 한 것만 불러오기
    other_answer_set = answer_set.exclude(user=request.user)    #자기 답은 제외
    return render(request, 'qna/other_people.html', {
            'question':question,
            'answer_set':other_answer_set,
        })

@login_required
def other_people(request):
    today_id = get_today_id()
    question = Question.objects.get(id=today_id)    #오늘의 질문 불러오기

    answer_set = Answer.objects.filter(question=question, is_public=True)   #공유한다고 한 것만 불러오기
    other_answer_set = answer_set.exclude(user=request.user)#자기 답은 제외

    page = request.GET.get('page', 1)
    paginator = Paginator(other_answer_set, 12)

    try:
        other_answer = paginator.page(page)
    except PageNotAnInteger:
        other_answer = paginator.page(1)
    except EmptyPage:
        other_answer = paginator.page(paginator.num_pages)


    return render(request, 'qna/other_people.html', {
            'question':question,
            'answer_set':other_answer_set,
            'other_answer': other_answer
        })
