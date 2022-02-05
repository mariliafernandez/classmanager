from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .permissions import ActionBasedPermission
from .models import  Subject, Professor,  Schedule
from .serializers import SubjectSerializer, ScheduleSerializer, StudentsClassSerializer, CreateProfessorSerializer, ProfessorRankingSerializer
from .controller import update_ranking, list_ranking


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
    serializer_class = CreateProfessorSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class SchedulesViewSet(viewsets.ModelViewSet):

    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [ActionBasedPermission]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    action_permissions = {
        IsAuthenticated: ['list'],
        IsAdminUser: ['update', 'partial_update', 'destroy', 'create', 'list'],
    }


class StudentsClassViewSet(viewsets.ModelViewSet):

    queryset = Schedule.objects.all()
    serializer_class = StudentsClassSerializer
    permission_classes = [ActionBasedPermission]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    action_permissions = {
        IsAuthenticated: ['list'],
        IsAdminUser: ['update', 'partial_update', 'destroy', 'create', 'list'],
    }


@api_view(['GET', 'POST'])
def ranking_view(request):

    if request.method == 'POST':
        serializer = ProfessorRankingSerializer(data=request.data, many=True)
        if serializer.is_valid(raise_exception=True):
            new_rank = update_ranking(serializer.validated_data).values()
            return Response(new_rank)

    elif request.method == 'GET':
        rank = list_ranking().values()
        return Response(rank)