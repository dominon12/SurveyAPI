from django.db import models


class Survey(models.Model):
    """Survey representation.
    """

    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Question(models.Model):
    """Survey's question respresentation.
    """

    QUESTION_TYPE_CHOICES = (
        (1, 'Text answer'),
        (2, 'One choice answer'),
        (3, 'Multiple choices answer')
    )

    survey = models.ForeignKey(
        Survey, 
        on_delete=models.CASCADE, 
        related_name='questions')
    text = models.TextField()
    question_type = models.IntegerField(choices=QUESTION_TYPE_CHOICES)

    def __str__(self):
        return self.text


class AnswerChoice(models.Model):
    """Represantation of question's 
    answer's choice.
    """

    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        related_name='choices')
    text = models.TextField()

    def __str__(self):
        return self.text


class CompletedSurvey(models.Model):
    """Representation of survey, 
    completed by the user.
    """

    user_id = models.IntegerField(null=True, blank=True)
    survey = models.ForeignKey(
        Survey, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='completed_surveys')

    def __str__(self):
        return f"{self.user_id} - {self.survey.name}"
    

class Answer(models.Model):
    """Representations of question's answer.
    """

    completed_survey = models.ForeignKey(
        CompletedSurvey,
        on_delete=models.CASCADE,
        related_name='answers')
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers')
    text_answer = models.TextField(blank=True)
    answer_choices = models.ManyToManyField(AnswerChoice, blank=True)

    def __str__(self):
        return f"Answer for survey '{str(self.completed_survey)}' made by user {self.completed_survey.user_id}"