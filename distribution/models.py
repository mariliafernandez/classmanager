from django.db import models
from datetime import date, time
from django.contrib.auth.models import User


class DayPeriod(models.TextChoices):
    MANHÃ = "MANHÃ"
    TARDE = "TARDE"
    NOITE = "NOITE"  


class KnowlegeArea(models.TextChoices):
    BIOLÓGICAS = "BIOLÓGICAS"
    EXATAS = "EXATAS"
    HUMANAS = "HUMANAS"
    ARTES = "ARTES"
    LINGUAS = "LÍNGUAS"
    OUTRAS = "OUTRAS"


class RequestStatus(models.TextChoices):
    CRIADO = "CRIADO"
    ACEITO = "ACEITO"
    NEGADO = "NEGADO"


class DistributionPhases(models.TextChoices):
    CARGA_DE_DADOS = "CARGA DE DADOS"
    REQUERIMENTOS = "REQUERIMENTOS"
    DISTRIBUIÇÃO = "DISTRIBUIÇÃO"


class Professor(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True, primary_key=True)
    area = models.TextField(choices=KnowlegeArea.choices)
    workload = models.PositiveSmallIntegerField(default=40)
    position = models.PositiveSmallIntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.user.email}"
    

class Schedule(models.Model):
    
    distribution = models.ForeignKey('Distribution', on_delete=models.CASCADE)
    time_slot = models.ForeignKey('TimeSlot', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    student_class = models.ForeignKey('StudentsClass', on_delete=models.CASCADE)
    professor = models.ForeignKey('Professor', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = [['student_class', 'time_slot'], ['professor', 'time_slot']]


class TimeSlot(models.Model):

    class Week(models.IntegerChoices):
        SEGUNDA_FEIRA = 2
        TERÇA_FEIRA = 3
        QUARTA_FEIRA = 4
        QUINTA_FEIRA = 5
        SEXTA_FEIRA = 6

    code = models.CharField(max_length=5, unique=True, null=True, blank=True)
    weekday = models.IntegerField(choices=Week.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    period = models.CharField(max_length=5, choices=DayPeriod.choices, null=True, blank=True)
    available = models.BooleanField(default=True)

    class Meta:
        unique_together = [['weekday', 'start_time', 'end_time']]

    def save(self, *args, **kwargs):
        
        if not self.period:
            if self.end_time.hour < 12:
                self.period = DayPeriod.MANHÃ
            elif self.end_time.hour < 18:
                self.period = DayPeriod.TARDE
            else:
                self.period = DayPeriod.NOITE

        if not self.code:
            self.code = f"{self.weekday}{self.period[0]}{self.start_time.hour}{self.start_time.minute}"
                
        super(TimeSlot, self).save(*args, **kwargs)
        

    def __str__(self):
        return self.code


class Subject(models.Model):

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=20)
    area = models.TextField(choices=KnowlegeArea.choices)

    def __str__(self):
        return self.name


class ProfessorScheduleOptions(models.Model):

    class Meta:
        unique_together = [['professor', 'schedule']]

    professor = models.ForeignKey('Professor', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE)
    status = models.TextField(choices=RequestStatus.choices, default=RequestStatus.CRIADO)


class StudentsClass(models.Model):

    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    grade = models.PositiveSmallIntegerField()
    subclass = models.CharField(max_length=2, null=True)
    period = models.TextField(choices=DayPeriod.choices, null=True)

    def __str__(self):
        return f"{self.grade}º {self.subclass} - {self.period}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code =  f"{self.grade}{self.subclass}{self.period[0]}"
        super(StudentsClass, self).save(*args, **kwargs)


class Distribution(models.Model):

    status = models.IntegerField(choices=DistributionPhases.choices, default=DistributionPhases.CARGA_DE_DADOS)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)