from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_list_or_404, get_object_or_404

from .models import Survey, Question, CompletedSurvey
from .serializers import (
    SurveySerializer, 
    QuestionSerializer, 
    CompletedSurveySerializer, 
    ParticularQuestionSerializer,
)


class SurveyViewSet(viewsets.ViewSet):
    """ViewSet for retrieving list / 
    adding / updating / deleting surveys.
    """
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()
    authentication_classes = (TokenAuthentication,)

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        survey = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(survey, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        survey = get_object_or_404(self.queryset, pk=pk)
        survey.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class QuestionViewSet(viewsets.ViewSet):
    """ViewSet for adding / updating / 
    deleting questions.
    """
    serializer_class = ParticularQuestionSerializer
    queryset = Question.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        qs = self.queryset.filter(date_ended=None)
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        question = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        question = get_object_or_404(self.queryset, pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateCompletedSurvey(CreateAPIView):
    """Creates a new 
    question's answer.
    """
    queryset = CompletedSurvey.objects.all()
    serializer_class = CompletedSurveySerializer


class CompletedSurveyList(ListAPIView):
    """Returns a list with all the
    surveys, completed by 
    the requested user.
    """
    queryset = CompletedSurvey.objects.all()
    serializer_class = CompletedSurveySerializer

    def get_queryset(self, *args, **kwargs):
        original_qs = super().get_queryset(*args, **kwargs)
        filtered_qs = get_list_or_404(
            original_qs, 
            user_id=self.kwargs.get("user_id")
        )
        return filtered_qs