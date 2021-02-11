from rest_framework import serializers

from .models import Survey, Question, Answer, CompletedSurvey


class ParticularQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('pk', 'text', 'question_type', 'survey')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('pk', 'text', 'question_type')


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    
    class Meta:
        model = Survey
        fields = (
            'pk', 
            'name', 
            'description', 
            'date_started', 
            'date_ended', 
            'questions'
        )

    def create(self, validated_data):
        questions = validated_data.pop('questions')
        if not questions:
            raise serializers.ValidationError({"questions": "This field is required"})
        survey = Survey.objects.create(**validated_data)
        for question in questions:
            Question.objects.create(
                survey=survey, 
                text=question.get('text'), 
                question_type=question.get('question_type')
            )
        return survey

    def update(self, instance, validated_data):
        questions = validated_data.pop('questions')
        survey = super().update(instance, validated_data)
        return survey


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('question', 'answer')


class CompletedSurveySerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    
    class Meta:
        model = CompletedSurvey
        fields = ('survey', 'user_id', 'answers')

    def create(self, validated_data):
        answers = validated_data.pop('answers')
        completed_survey = CompletedSurvey.objects.create(**validated_data)
        for answer in answers:
            Answer.objects.create(
                completed_survey=completed_survey, 
                question=answer.get('question'), 
                answer=answer.get('answer')
            )
        return completed_survey