from django.shortcuts import render
from django.http import HttpResponse
from .models import Question, Answer
import time

def question(request):
    queryset = Question.objects.all()
    #days=time.strftime('%j', time.localtime(time.time()))
    days='3'
#days에 걸리는 함수를 통해 오늘이 365일 중에 몇 번째 날인지 파악
#그날에 맞는 질문을 골라 온다.
    return render(request, 'diary/index.html', {
        })
#question.html에 그날의 질문과 질문의 날짜를 변수로 보낸다.

def answer_submit(request, id):

    if request.POST:
        answer = request.POST['answer']
#post방식으로 들어오면 answer라고 받은 값을 answer에 넘긴다.
        queryset = Question.objects.all()
        q_idx=queryset.get(id=id)
        queryset = Answer.objects.create(question=q_idx ,content= answer)
#전체 질문 중에 question.id로 받은 id와 같은 question을 불러와서 그 question과 content를 create함수로 저장한다.

        return render(request, 'qna/answer_submit.html',{
            'answer': answer,
            'question':q_idx,
            })
#answer_submit.html로 이동하면서 변수 두개를 넘긴다.

#form강의 듣고 view 함수 구현해보기!
