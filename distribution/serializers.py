from .models import Subject, Professor, Schedule, StudentsClass

from rest_framework import serializers

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        exclude = []


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        exclude = []


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        exclude = []


class StudentsClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentsClass
        exclude = ['code']