from django.urls import path
from rest_framework import routers

from .views import ProfessorsViewSet, SubjectsViewSet, SchedulesViewSet

router = routers.SimpleRouter()
router.register(r'subjects', SubjectsViewSet, basename='subject')
router.register(r'professors', ProfessorsViewSet, basename='professor')
router.register(r'schedules', SchedulesViewSet, basename='schedule')