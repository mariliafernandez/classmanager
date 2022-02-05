from .models import Subject, Professor, Schedule, StudentsClass

from rest_framework import serializers

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class CreateProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class StudentsClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentsClass
        exclude = ['code']


class ProfessorRankingSerializer(serializers.Serializer):

    professor_code = serializers.CharField(max_length=10)
    professor_position = serializers.IntegerField()

    def validate_professor_code(self, professor_code):
        
        try:
            Professor.objects.get(code=professor_code)
            return professor_code
        except(Professor.DoesNotExist):
            print(professor_code)
            raise serializers.ValidationError(f"Não existe professor com este código: {professor_code}")

    def validate_professor_position(self, professor_position):

        professors_count = Professor.objects.count()
        if professor_position > professors_count:
            raise serializers.ValidationError(f"A posição deve ser no máximo {professors_count}.")
        if professor_position <= 0:
            raise serializers.ValidationError(f"A posição deve ser maior que zero.")

        return professor_position