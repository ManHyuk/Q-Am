<<<<<<< HEAD
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Question, Answer
import time
from .forms import AnswerForm

=======
# qna/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question, Answer
# import time
from .forms import AnswerForm
from django.utils import timezone
>>>>>>> fe062aba711e97ab9684214deeaf660b700fb40e


def main(request):
    # answers = Answer.objects.filter()
    return render(request, 'qna/main.html')

def question(request,user_id):
    #days=time.strftime('%j', time.localtime(time.time()))
<<<<<<< HEAD
    days='3'
    #days에 걸리는 함수를 통해 오늘이 365일 중에 몇 번째 날인지 파악
    now=int(days)
    ques=queryset.get(id=now)
    #그날에 맞는 질문을 골라 온다.
=======
    days='1'
    #days에 걸리는 함수를 통해 오늘이 365일 중에 몇 번째 날인지 파악
    now=int(days)
    ques=Question.objects.get(id=now)
    #그날에 맞는 질문을 골라 온다.
    already_answer = Answer.objects.filter(question_id=now, created_at__year=timezone.now().year)   #오늘 이미 답변했으면 넘어가기
    if already_answer:
        redirect('exqna:exquestion', user_id=user_id)
>>>>>>> fe062aba711e97ab9684214deeaf660b700fb40e

    if request.method=='POST':
        form=AnswerForm(request.POST,request.FILES)
        if form.is_valid():
<<<<<<< HEAD
            answer=form.save()
            return redirect('qna:question_submit')
    else :
        form = AnswerForm()
    return render(request, 'qna/question.html', {
        'form':form,
        'question' : ques,
        'question_at' : ques.questioned_at,
        })

def question_submit(request,id):
    question=get_object_or_404(Question,id=id)
    return render(request, 'qna/submit.html', {
        'question' : question,

        })
#     if request.POST:

# #post방식으로 들어오면 answer라고 받은 값을 answer에 넘긴다.
#         queryset = Question.objects.all()
#         q_idx=queryset.get(id=id)
#         queryset = Answer.objects.create(question=q_idx ,content= answer)
# #전체 질문 중에 question.id로 받은 id와 같은 question을 불러와서 그 question과 content를 create함수로 저장한다.

#         return render(request, 'qna/submit.html',{
#             'content': answer,
#             'question':q_idx,
#             })

def question_edit(request, id):
    answer=get_object_or_404(Answer, id=id)
    if request.method=='POST':
        form=AnswerForm(request.POST,request.FILES,instance=answer)
        if form.is_valid():
            answer=form.save()
            return render(request,'qna/question_edit.html')

    else :
        form = AnswerForm(instance=answer)

    return render(request, 'qna/question.html', {
        'form':form,
        })
=======
            answer=form.save(commit=False)
            answer.user_id = user_id
            answer.question = ques
            answer.save()
            return redirect('exqna:exquestion', user_id=user_id)
    else :
        form = AnswerForm()
    return render(request, 'qna/question.html', {
            'form':form,
            'question' : ques,
        })

def question_edit(request, answer_id):
    answer=get_object_or_404(Answer,id=answer_id)
    if answer.created_at.hour + 1 > timezone.now().hour:    #1시간 지났을 경우 수정 불가
        return redirect('qna:main')
    if request.method=='POST':
        form=AnswerForm(request.POST,request.FILES,instance=answer)
        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.user_id = answer.user_id
            new_answer.question = answer.question
            new_answer.save()
            return redirect('qna:main')
    else :
        form = AnswerForm(instance=answer)
    return render(request, 'qna/question_edit.html', {
            'form':form,
            'answer':answer,
        })

>>>>>>> fe062aba711e97ab9684214deeaf660b700fb40e
