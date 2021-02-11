from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SurveyViewSet, QuestionViewSet, CreateCompletedSurvey, CompletedSurveyList


app_name = 'surveys'


urlpatterns = [
    path('list/', SurveyViewSet.as_view({'get': 'list'}), name='list'),
    path('create/', SurveyViewSet.as_view({'post': 'create'}), name='create'),
    path('<pk>/destroy/', SurveyViewSet.as_view({'delete': 'destroy'}), name='destroy'),
    path('<pk>/update/', SurveyViewSet.as_view({'put': 'update'}), name='update'),
    path('questions/list/', QuestionViewSet.as_view({'get': 'list'}), name='questions_list'),
    path('questions/create/', QuestionViewSet.as_view({'post': 'create'}), name='questions_create'),
    path('questions/<pk>/destroy/', QuestionViewSet.as_view({'delete': 'destroy'}), name='questions_destroy'),
    path('questions/<pk>/update/', QuestionViewSet.as_view({'put': 'update'}), name='questions_update'),
    path('completed/create/', CreateCompletedSurvey.as_view(), name='create_completed_survey'),
    path('completed/<int:user_id>/', CompletedSurveyList.as_view(), name='get_completed_surveys')
]
