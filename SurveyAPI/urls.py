from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from surveys import views as surveys_views

router = DefaultRouter()
router.register('surveys', surveys_views.SurveyViewSet)
router.register('questions', surveys_views.QuestionViewSet)
router.register('completed-surveys', surveys_views.CompletedSurveyViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v0.1/accounts/', include('accounts.urls', namespace='accounts')),
    path('api/v0.1/', include((router.urls, 'surveys'), namespace='surveys'))
]
