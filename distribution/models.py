from django.db import models
from datetime import date

from django.contrib.auth.models import User

AREAS = [(1,'EXATAS'), (2, 'BIOLÓGICAS'), (3, 'HUMANAS'), (4, 'ARTES'), (5, 'LETRAS')]
PERIOD_CHOICES = [('M', 'MANHÃ'), ('T', 'TARDE'), ('N', 'NOITE')]


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True, primary_key=True)
    area = models.IntegerField(choices=AREAS)
    workload = models.PositiveSmallIntegerField(default=40)
    position = models.PositiveSmallIntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.user.email}"
    

class Schedule(models.Model):
    
    distribution = models.OneToOneField('Distribution', on_delete=models.CASCADE)
    time_slot = models.ForeignKey('TimeSlot', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    student_class = models.ForeignKey('StudentsClass', on_delete=models.CASCADE)
    professor = models.ForeignKey('Professor', on_delete=models.CASCADE)


class TimeSlot(models.Model):
    WEEKDAYS = [
        (2, 'Segunda-feira'),
        (3, 'Terça-feira'),
        (4, 'Quarta-feira'),
        (5, 'Quinta-feira'),
        (6, 'Sexta-feira'),
    ]
    code = models.CharField(max_length=5, unique=True, null=True, blank=True)
    weekday = models.IntegerField(choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    period = models.CharField(max_length=1, choices=PERIOD_CHOICES, null=True)
    available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f"{self.weekday}{self.period}{self.start_time.hour}{self.start_time.minute}"
        super(TimeSlot, self).save(*args, **kwargs)
        

    def __str__(self):
        return self.code


class Subject(models.Model):

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=20)
    area = models.IntegerField(choices=AREAS)

    def __str__(self):
        return self.name


class ProfessorScheduleOptions(models.Model):
    STATUS_CHOICES = [
        ('E', 'EM ANÁLISE'),
        ('A', 'ACEITO'),
        ('N', 'NEGADO')
    ]
    professor = models.ForeignKey('Professor', on_delete=models.CASCADE)
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, null=True)


class StudentsClass(models.Model):

    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    grade = models.PositiveSmallIntegerField()
    subclass = models.CharField(max_length=2, null=True)
    period = models.CharField(max_length=1, choices=PERIOD_CHOICES, null=True)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code =  f"{self.grade}{self.subclass}{self.period}"
        super(StudentsClass, self).save(*args, **kwargs)


class Distribution(models.Model):
    STATUS_CHOICES = [
        ('L', 'LOAD'),
        ('C', 'CREATE'),
        ('R', 'RESULTS')
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_CHOICES[0])
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)