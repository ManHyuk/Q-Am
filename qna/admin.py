from django.contrib import admin
from .models import Question,Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display=['user','question','content','is_public','created_at','updated_at']
=======
    list_display=['user','question','content','photo','is_public','created_at','updated_at']

>>>>>>> fe062aba711e97ab9684214deeaf660b700fb40e
