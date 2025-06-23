from datetime import timedelta

from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.utils.datetime_safe import datetime
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Projects, ParticipationInProjects, Events, ParticipationInEvents, ParticipationResults, Student
from .serializers import StudentSerializer, ProjectsSerializer, ParticipationInProjectsSerializer, EventsSerializer, \
    ParticipationInEventsSerializer, ParticipationResultsSerializer


def IndexView(request):
    student_list = Student.objects.all()
    context = {"student_list": student_list}
    return render(request, "main/index.html", context)


def DetailView(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        raise Http404("Student does not exist")
    return render(request, "main/detail.html", {"student": student})


def ResultsView(request, student_id):
    response = "Результаты студента %s."
    return HttpResponse(response % student_id)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = Student.objects.all()

        # Фильтрация по курсу и запросу с использованием Q
        course = self.request.query_params.get('course', None)
        search_query = self.request.query_params.get('search', None)

        if course:
            queryset = queryset.filter(course=course)

        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )

        return queryset

    @action(detail=False, methods=['GET'])
    def younger_than(self, request):
        age_limit = request.query_params.get('age_limit', None)

        if age_limit is None:
            return Response({"error": "Пожалуйста, укажите параметр 'age_limit'"}, status=status.HTTP_400_BAD_REQUEST)

        today = datetime.today()
        age_limit = int(age_limit)

        filtered_students = self.queryset.filter(
            date_of_birth__gt=(today - timedelta(days=365 * age_limit))
        )

        serializer = self.get_serializer(filtered_students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer


class ParticipationInProjectsViewSet(viewsets.ModelViewSet):
    queryset = ParticipationInProjects.objects.all()
    serializer_class = ParticipationInProjectsSerializer


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer


class ParticipationInEventsViewSet(viewsets.ModelViewSet):
    queryset = ParticipationInEvents.objects.all()
    serializer_class = ParticipationInEventsSerializer


class ParticipationResultsViewSet(viewsets.ModelViewSet):
    queryset = ParticipationResults.objects.all()
    serializer_class = ParticipationResultsSerializer

