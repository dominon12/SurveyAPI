from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, AllowAny
from django.utils import timezone

from .models import (
    Survey, 
    Question, 
    AnswerChoice,
    CompletedSurvey)
from .serializers import (
    SurveySerializer, 
    QuestionSerializer, 
    AnswerChoiceSerializer,
    CompletedSurveySerializer)



class QuestionViewSet(viewsets.ModelViewSet):
    """Question ViewSet.
    """
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]


class SurveyViewSet(viewsets.ModelViewSet):
    """Survey ViewSet.
    """
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if self.action == 'list' and not self.request.user.is_staff:
            # show surveys to not staff users with 
            # end_date greater or equal than actual date
            return self.queryset.filter(end_date__gte=timezone.now())
        return super().get_queryset()

    def get_permissions(self):
        """Allow access to list of surveys to
        unauthorized users.
        """
        if self.action == 'list':
            return [AllowAny()]
        return [permission() for permission in self.permission_classes]


class CompletedSurveyViewSet(viewsets.ModelViewSet):
    """CompletedSurvey ViewSet.
    """
    serializer_class = CompletedSurveySerializer
    queryset = CompletedSurvey.objects.all()

    def list(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        if user_id:
            try:
                user_id = int(user_id)
            except ValueError:
                return Response({"message": "Incorrect user_id"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                self.queryset = self.queryset.filter(user_id=user_id)
        return super().list(request, *args, **kwargs)