from django.urls import path
from rest_framework import routers

from .views import ProfessorsViewSet, SubjectsViewSet, SchedulesViewSet, RankingViewSet, ProfessorScheduleOptionsViewSet

router = routers.DefaultRouter()
router.register(r'subjects', SubjectsViewSet, basename='subject')
router.register(r'schedules', SchedulesViewSet, basename='schedule')
router.register(r'professors', ProfessorsViewSet, basename='professor')
router.register(r'ranking', RankingViewSet, basename='ranking')
router.register(r'my-schedule-options', ProfessorScheduleOptionsViewSet, basename='my-schedule-options')

urlpatterns = router.urls