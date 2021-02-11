from django.contrib import admin

from .models import Survey, Question, Answer, CompletedSurvey



@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("pk", "__str__", "date_answered")
    search_fields = ("answer",)
    readonly_fields = ("date_answered",)
    list_filter = ("date_answered",)

    class Meta:
        model = Answer


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0


@admin.register(CompletedSurvey)
class CompletedSurveyAnswer(admin.ModelAdmin):
    list_display = ("pk", "__str__", "user_id", "answers_num", "date_ended")
    search_fields = ("survey",)
    readonly_fields = ("date_ended",)
    inlines = (AnswerInline,)

    class Meta:
        model = CompletedSurvey


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("pk", "__str__", "get_question_type_display", "answers_num")
    search_fields = ("survey__name", "text")
    list_filet = ("get_question_type_display",)
    inlines = (AnswerInline,)

    class Meta:
        model = Question


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name", 
        "date_started", 
        "date_ended", 
        "questions_num"
    )
    readonly_fields = ("date_started",)
    list_filter = ("date_started", "date_ended")
    search_fields = ("name", "description")
    inlines = (QuestionInline,)

    class Meta:
        model = Survey