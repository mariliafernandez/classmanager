from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework import status

from .permissions import ActionBasedPermission
from .models import  Subject, Professor, Schedule, ProfessorScheduleOptions
from .serializers import SubjectSerializer, ScheduleSerializer, StudentsClassSerializer, CreateProfessorSerializer, ProfessorRankingSerializer, InputProfessorScheduleOptionsSerializer, TimeSlotSerializer
from .controller import distribute_classes, update_ranking, list_ranking, list_professor_schedule_options, get_professor_by_username, create_professor_schedule_options


class SubjectsViewSet(viewsets.ModelViewSet):

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [ActionBasedPermission]

    action_permissions = {
        IsAuthenticated: ['list'],
        IsAdminUser: ['update', 'partial_update', 'destroy', 'create', 'list'],
    }

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({'subjects': serializer.data}, template_name='distribution/index.html')


class ProfessorsViewSet(viewsets.ModelViewSet):

    queryset = Professor.objects.all()
    serializer_class = CreateProfessorSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class SchedulesViewSet(viewsets.GenericViewSet):

    queryset = Schedule.objects.all().order_by('id')
    serializer_class = ScheduleSerializer
    permission_classes = [ActionBasedPermission]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    action_permissions = {
        IsAuthenticated: ['list'],
        IsAdminUser: ['update', 'partial_update', 'destroy', 'create', 'list'],
    }

    def list(self, request):

        if request.user.is_superuser:
            print("is superuser")
            qs = distribute_classes()
        else:
            qs = self.get_queryset()
        
        result = []

        for item in qs:
            
            result.append({
                "distribution":item.distribution.id,
                "time_slot": {
                    "code": item.time_slot.code,
                    "weekday": item.time_slot.weekday,
                    "start_time": item.time_slot.start_time,
                    "end_time": item.time_slot.end_time,
                    "period": item.time_slot.period,
                    "available": item.time_slot.available,
                },
                "subject": {
                    "code": item.subject.code,
                    "name": item.subject.name,
                    "area": item.subject.area,
                },
                "class": {
                    "code": item.student_class.code,
                    "grade": item.student_class.grade,
                    "subclass": item.student_class.subclass,
                    "period": item.student_class.period,
                },
                "professor": str(item.professor) if item.professor else None,
            })

    
        return Response(result)


class StudentsClassViewSet(viewsets.ModelViewSet):

    queryset = Schedule.objects.all()
    serializer_class = StudentsClassSerializer
    permission_classes = [ActionBasedPermission]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    action_permissions = {
        IsAuthenticated: ['list'],
        IsAdminUser: ['update', 'partial_update', 'destroy', 'create', 'list'],
    }


class RankingViewSet(viewsets.ModelViewSet):
    
    queryset = Professor.objects.all().order_by('position')
    permission_classes = [IsAdminUser]
    serializer_class = ProfessorRankingSerializer

    def create(self, request):

        serializer = self.get_serializer(data=request.data, many=True)

        if serializer.is_valid(raise_exception=True):
            new_rank = update_ranking(serializer.validated_data).values()
            return Response(new_rank)

    def list(self, request):

        rank = list_ranking().values()
        return Response(rank)


class ProfessorScheduleOptionsViewSet(viewsets.ModelViewSet):

    queryset = ProfessorScheduleOptions.objects.all()

    action_permissions = {
        IsAuthenticated: ['list', 'create', 'update', 'partial_update'],
        IsAdminUser: ['list']
    }


    def list(self, request):

        professor = get_professor_by_username(request.user)
        professor_schedule_options = list_professor_schedule_options(professor).values()
        return Response(professor_schedule_options)


    def create(self, request):
        
        serializer = InputProfessorScheduleOptionsSerializer(data=request.data, many=True)

        if serializer.is_valid(raise_exception=True):
            professor = get_professor_by_username(request.user)
            create_professor_schedule_options(professor, request.user, serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)


