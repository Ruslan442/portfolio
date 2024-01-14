from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import (StudentViewSet, ProjectsViewSet, ParticipationInProjectsViewSet, EventsViewSet,
                    ParticipationInEventsViewSet, ParticipationResultsViewSet)

app_name = "main"

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'projects', ProjectsViewSet)
router.register(r'participation-in-projects', ParticipationInProjectsViewSet)
router.register(r'events', EventsViewSet)
router.register(r'participation-in-events', ParticipationInEventsViewSet)
router.register(r'participation-results', ParticipationResultsViewSet)

urlpatterns = [
                  # path("", views.IndexView, name="index"),
                  # path("<int:student_id>/", views.DetailView, name="detail"),
                  # path("<int:student_id>/results/", views.ResultsView, name="results"),
              ] + router.urls
