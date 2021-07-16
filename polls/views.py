from rest_framework import viewsets

from .serializers import PollSerializer, QuestionSerializer, SurveySerializer

from .models import Poll, Question, Survey

import datetime
from rest_framework.permissions import SAFE_METHODS, BasePermission

from django_filters.rest_framework import DjangoFilterBackend
import django_filters


class PollPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        view.queryset = view.queryset.filter(
            end_date__gte=datetime.date.today()
        )
        if request.method.upper() in SAFE_METHODS:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class QuestionPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class SurveyFilter(django_filters.FilterSet):

    class Meta:
        model = Survey
        fields = {
            'user': ['exact', 'isnull'],
            'poll': ['exact'],
        }


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (PollPermission, )


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (QuestionPermission, )


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    filter_backends = (DjangoFilterBackend, )
    http_method_names = ('get', 'post')
    filterset_class = SurveyFilter

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            return serializer.save(user=self.request.user)

        return super().perform_create(serializer)
