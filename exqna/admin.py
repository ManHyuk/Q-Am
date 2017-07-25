from django.contrib import admin
from .models import ExtraQuestion, ExtraAnswer

@admin.register(ExtraQuestion)
class ExtraQuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'questioned_at']

@admin.register(ExtraAnswer)
class ExtraAnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'is_public']
