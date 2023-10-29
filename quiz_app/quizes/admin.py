from django.contrib import admin

import nested_admin as n_admin

from .models import Quiz, Question, Answer, QuizOpinion

class AnswerAdminInLine(n_admin.NestedStackedInline):
    model = Answer
    extra = 0
    max_num = 10
    min_num = 2

class QuestionAdminInline(n_admin.NestedStackedInline):
    model = Question
    extra = 0
    min_num = 1
    inlines = [AnswerAdminInLine]

class QuizOpinionInline(n_admin.NestedStackedInline):
    model = QuizOpinion
    extra = 0

class QuizAdmin(n_admin.NestedModelAdmin):
    inlines = [QuestionAdminInline, QuizOpinionInline]
    readonly_fields = ('solves',)

admin.site.register(Quiz, QuizAdmin)