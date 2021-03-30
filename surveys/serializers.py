from rest_framework import serializers

from .models import Survey, Question, AnswerChoice, CompletedSurvey, Answer
from . import service



class AnswerChoiceSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=False)

    class Meta:
        model = AnswerChoice
        fields = [
            'pk',
            'question',
            'text'
        ]
        read_only_fields = ['question']


class QuestionSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=False)
    choices = AnswerChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = [
            'pk',
            'text',
            'survey',
            'question_type',
            'choices'
        ]

    def create(self, validated_data):
        return service.create_question(validated_data)

    def update(self, instance, validated_data):
        return service.update_question(instance, validated_data)


class SurveyQuestionSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=False)
    choices = AnswerChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = [
            'pk',
            'text',
            'question_type',
            'choices'
        ]


class SurveySerializer(serializers.ModelSerializer):
    questions = SurveyQuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = [
            'pk',
            'name',
            'description',
            'start_date',
            'end_date',
            'questions'
        ]

    def create(self, validated_data):
        questions = validated_data.pop('questions')
        survey = Survey.objects.create(**validated_data)
        [service.create_question(question, survey=survey) for question in questions]
        return survey

    def update(self, instance, validated_data):
        return service.update_survey(instance, validated_data)


class AnswerSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=False)
    answer_choices = serializers.PrimaryKeyRelatedField(
        queryset=AnswerChoice.objects.all(), 
        many=True, 
        required=False)

    class Meta:
        model = Answer
        fields = [
            'pk',
            'question',
            'text_answer',
            'answer_choices'
        ]


class CompletedSurveySerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = CompletedSurvey
        fields = [
            'pk',
            'user_id',
            'survey',
            'answers'
        ]

    def create(self, validated_data):
        return service.create_completed_survey(validated_data)
