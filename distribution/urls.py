from django.urls import path
from rest_framework import routers

from .views import ProfessorsViewSet, SubjectsViewSet, SchedulesViewSet, ranking_view

router = routers.DefaultRouter()
router.register(r'subjects', SubjectsViewSet, basename='subject')
router.register(r'schedules', SchedulesViewSet, basename='schedule')
router.register(r'professors', ProfessorsViewSet, basename='professor')

urlpatterns = router.urls
urlpatterns += [
    path(r'ranking/', ranking_view)
]