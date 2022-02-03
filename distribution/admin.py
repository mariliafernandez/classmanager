from ast import Sub
from django.contrib import admin

from .models import Professor, Schedule, Subject, StudentsClass, Distribution, TimeSlot

admin.site.register(Professor)
admin.site.register(Schedule)
admin.site.register(Subject)
admin.site.register(TimeSlot)
admin.site.register(Distribution)
admin.site.register(StudentsClass)
