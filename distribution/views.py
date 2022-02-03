from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import SubjectSerializer, ProfessorSerializer, ScheduleSerializer, StudentsClassSerializer
from .models import  Subject, Professor,  Schedule, StudentsClass
from .permissions import ActionBasedPermission

class SubjectsViewSet(viewsets.ModelViewSet):

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [ActionBasedPermission]

    action_permissions = {
        IsAuthenticated: ['list'],
        IsAdminUser: ['update', 'partial_update', 'destroy', 'create', 'list'],
    }


class ProfessorsViewSet(viewsets.ModelViewSet):

    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAdminUser]


class SchedulesViewSet(viewsets.ModelViewSet):

    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [ActionBasedPermission]

    action_permissions = {
        IsAuthenticated: ['list'],
        IsAdminUser: ['update', 'partial_update', 'destroy', 'create', 'list'],
    }


class StudentsClassViewSet(viewsets.ModelViewSet):

    queryset = Schedule.objects.all()
    serializer_class = StudentsClassSerializer
    permission_classes = [ActionBasedPermission]

    action_permissions = {
        IsAuthenticated: ['list'],
        IsAdminUser: ['update', 'partial_update', 'destroy', 'create', 'list'],
    }