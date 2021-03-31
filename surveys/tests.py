from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth import get_user_model

from datetime import datetime
import pytz

from .views import (
    SurveyViewSet, 
    QuestionViewSet, 
    CompletedSurveyViewSet)
from .models import (
    Survey, 
    Question, 
    AnswerChoice, 
    CompletedSurvey, 
    Answer)


class SurveyTestCases(TestCase):
    def setUp(self):
        # setup request factory
        self.factory = APIRequestFactory()
        # create user
        self.user = get_user_model().objects.create_user(
            username='test',
            password='testtest',
            is_staff=True)
        # set timezone
        self.utc_timezone = pytz.timezone("UTC")
        # setup data
        self.create_survey_payload = {
            "name": "Favourite colors poll!",
            "description": "This survey will ask you about your favourite color",
            "start_date": "2021-01-01T00:00:00.000Z",
            "end_date": "2021-12-31T00:00:00.000Z",
            "questions": [
                {
                    "text": "What is your favourite color?",
                    "question_type": 2,
                    "choices": [
                        {"text": "Red"},
                        {"text": "Blue"},
                        {"text": "Green"}
                    ]
                },
                {
                    "text": "Why do you like it?",
                    "question_type": 1,
                    "choices": []
                },
                {
                    "text": "Select some other colors that you may like",
                    "question_type": 3,
                    "choices": [
                        {"text": "White"},
                        {"text": "Pink"},
                        {"text": "Tiffany"}
                    ]
                }
            ]  
        }

    def test_create_survey(self):
        """Test survey creating.
        """
        view = SurveyViewSet.as_view({'post': 'create'})
        request = self.factory.post(
            '/api/v0.1/surveys/', 
            data=self.create_survey_payload, 
            format='json')
        force_authenticate(request, user=self.user)
        response = view(request)
        # status is equal to 201
        self.assertEqual(response.status_code, 201)
        survey_qs = Survey.objects.all()
        # only 1 survey has been created
        self.assertEqual(survey_qs.count(), 1)
        created_survey = survey_qs[0]
        # survey's start and end dates are correct
        expected_start_date = self.utc_timezone.localize(
            datetime(year=2021, month=1, day=1, hour=0, minute=0, second=0))
        self.assertEqual(created_survey.start_date, expected_start_date)
        expected_end_date = self.utc_timezone.localize(
            datetime(year=2021, month=12, day=31, hour=0, minute=0, second=0))
        self.assertEqual(created_survey.end_date, expected_end_date)
        questions_qs = created_survey.questions.all()
        # number of created questions is correct
        self.assertEqual(questions_qs.count(), 3)
        # questions' names are correct
        question_names = [q.text for q in questions_qs]
        self.assertIn("What is your favourite color?", question_names)
        self.assertIn("Why do you like it?", question_names)
        self.assertIn("Select some other colors that you may like", question_names)
        # check questions' types and answer choices
        question_of_2_type = questions_qs.get(text="What is your favourite color?")
        self.assertEqual(question_of_2_type.question_type, 2)
        self.assertEqual(question_of_2_type.get_question_type_display(), "One choice answer")
        self.assertEqual(question_of_2_type.choices.all().count(), 3)
        answer_choices_names = [choice.text for choice in question_of_2_type.choices.all()]
        self.assertIn("Red", answer_choices_names)
        self.assertIn("Blue", answer_choices_names)
        self.assertIn("Green", answer_choices_names)
        question_of_1_type = questions_qs.get(text="Why do you like it?")
        self.assertEqual(question_of_1_type.question_type, 1)
        self.assertEqual(question_of_1_type.get_question_type_display(), "Text answer")
        self.assertEqual(question_of_1_type.choices.all().count(), 0)
        question_of_3_type = questions_qs.get(text="Select some other colors that you may like")
        self.assertEqual(question_of_3_type.question_type, 3)
        self.assertEqual(question_of_3_type.get_question_type_display(), "Multiple choices answer")
        self.assertEqual(question_of_3_type.choices.all().count(), 3)
        answer_choices_names = [choice.text for choice in question_of_3_type.choices.all()]
        self.assertIn("White", answer_choices_names)
        self.assertIn("Pink", answer_choices_names)
        self.assertIn("Tiffany", answer_choices_names)