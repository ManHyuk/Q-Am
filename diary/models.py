from django.db import models
from django.conf import settings


class Diary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    title = models.CharField(max_length=10, null=False,verbose_name='제목')

    content = models.TextField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성 날짜')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
