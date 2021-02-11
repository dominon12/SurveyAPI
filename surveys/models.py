from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Survey(models.Model):
    """Model to represent survey.
    """
    name = models.CharField("Name", max_length=150)
    description = models.TextField("Description")
    date_started = models.DateTimeField("Date started", auto_now_add=True)
    date_ended = models.DateTimeField("Date ended", null=True, blank=True)

    class Meta:
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"

    def __str__(self):
        return self.name

    def questions_num(self):
        """Returns number of 
        survey's question.
        """
        return self.questions.all().count()
    questions_num.short_description = "Number of questions"


class Question(models.Model):
    """Model to represent Survey's question.
    """
    QUESTION_TYPE_CHOICES = (
        (1, "Text answer"),
        (2, "1 choice answer"),
        (3, "Multiple choices answer")
    )

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField("Text")
    question_type = models.IntegerField(
        "Question's type", 
        choices=QUESTION_TYPE_CHOICES, 
        validators=(
            MinValueValidator(1), 
            MaxValueValidator(3)
        )
    )

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.text

    def answers_num(self):
        """Returns number of answers,
        submitted by users.
        """
        return self.answers.all().count()
    answers_num.short_description = "Number of answers"



class CompletedSurvey(models.Model):
    """Model to represent survey, 
    completed by user.
    """
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user_id = models.BigIntegerField("User ID")
    date_ended = models.DateTimeField("Date ended", auto_now_add=True)

    class Meta:
        verbose_name = "Completed survey"
        verbose_name_plural = "Completed surveys"

    def __str__(self):
        return self.survey.name

    def answers_num(self):
        return self.answers.all().count()
    answers_num.short_description = "Number of answers"


class Answer(models.Model):
    """Model to represent answer
    on Survey's quesiton.
    """
    completed_survey = models.ForeignKey(CompletedSurvey, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer = models.TextField("Answer")
    date_answered = models.DateTimeField("Date answered", auto_now_add=True)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return str(self.question.survey.name)

