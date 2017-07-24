from django.contrib import admin
from .models import Question,Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display=['user','question','content','photo','is_public','created_at','updated_at']
