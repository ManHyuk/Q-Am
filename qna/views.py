from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Question, Answer
import time
from .forms import AnswerForm


def question(request):
    queryset = Question.objects.all()
    #days=time.strftime('%j', time.localtime(time.time()))
    days='3'
    #days에 걸리는 함수를 통해 오늘이 365일 중에 몇 번째 날인지 파악
    now=int(days)
    ques=queryset.get(id=now)
    #그날에 맞는 질문을 골라 온다.

    if request.method=='POST':
        form=AnswerForm(request.POST,request.FILES)
        if form.is_valid():
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