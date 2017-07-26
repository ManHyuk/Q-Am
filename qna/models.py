from django.db import models
from django.conf import settings
import time


class Question(models.Model):
    # 질문
    question = models.CharField(max_length=32, null=False, verbose_name='제목') # 제목
    month=models.CharField(max_length=2, null=False, verbose_name='달')
    day = models.CharField(max_length=2, null=False, verbose_name='월')
    def __str__(self):
        return self.question

    def get_today_id():#지금 시간에 해당하는 question id  return하는 함수
                        #왜 self 안쓰지???
        now = time.localtime()
        year_now = now.tm_year  #올해 몇년?
        is_leap_year = False    #윤년
        if year_now%4 == 0:
            is_leap_year = True
            if year_now&100 == 0:
                is_leap_year = False
                if year_now%400 == 0:
                    is_leap_year = True
        if is_leap_year:
            today_id = now.tm_yday
        else:
            if now.tm_mon <= 2:
                today_id = now.tm_yday
            else:
                today_id = now.tm_yday + 1
        if now.tm_hour < 4:     #새벽4시에 업데이트, so 그 전에는 같은 질문으로 뜨도록
            today_id = today_id - 1
        if not today_id:    #위 때문에 0이 되면 id가 366으로 리턴이 되게 함
            today_id = 366
        return today_id


class Answer(models.Model):
    # 답변
    user = models.ForeignKey(settings.AUTH_USER_MODEL) # 유저와 1:N 관계 설정
    question = models.ForeignKey(Question) # 질문 모델과 1:N 관계 설정
    content = models.TextField(max_length=256) # 답변 내용
    is_public = models.BooleanField(default=False) # 공개/비공개
    created_at = models.DateTimeField(auto_now_add=True) # 생성 날짜
    updated_at = models.DateTimeField(auto_now=True) # 수정 날짜
    def __str__(self):
        return '{}에 대한 {}의 답변{}'.format(self.question, self.user, self.content)

