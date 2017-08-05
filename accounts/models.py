from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import validate_email
from qna.models import Answer
from django.utils import timezone
from django.core.validators import RegexValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=10)
    nickname = models.CharField(unique=True, max_length=32, default=None)
    phone_number = models.CharField(max_length=20,validators=[RegexValidator(r'^010[1-9]\d{7}$')])
    email = models.EmailField(max_length=100)
    img = ProcessedImageField(
        upload_to='blog/%Y/%m/%d',
        blank=True,
        null=True,
        processors=[Thumbnail(100, 100)],  # 처리할 작업목록
        format='JPEG',
        options={'quality': 80}
    )





# def if_ok_answer():
#
#     answer_list=Answer.objects.filter(created_at__year=timezone.now().year, question__month=timezone.now().month, question__day=timezone.now().day)
#
#     user_list=User.objects.all()
#
#     user_id_total = []
#     for user_id in user_list:
#         user_id_total.append(user_id.id)
#
#     user_id_answer = []
#     for answer_id in answer_list:
#         user_id_answer.append(answer_id.user_id)
#
#     user_id_kakao = list(set(user_id_total).difference(user_id_answer))
    #답변안한 user_id 얻음

    #전화번호 받는 부분 만들기
    #그들의 전화번호를 얻음
    #문자를 보내는 곳으로 전화번호를 보냄

