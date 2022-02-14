from .models import Distribution, Professor, ProfessorScheduleOptions, RequestStatus, Schedule


def update_ranking(obj_list):

    clear_ranking()
    
    for obj in obj_list:
        p = Professor.objects.get(code=obj['professor_code'])
        p.position = obj['professor_position']
        p.save()
    return Professor.objects.all().order_by('position')


def list_ranking():
    return Professor.objects.all().order_by('position')


def clear_ranking():
    Professor.objects.filter(position__isnull=False).update(position=None)


def list_professor_schedule_options(professor):
    return ProfessorScheduleOptions.objects.filter(professor=professor).order_by('id')


def get_professor_by_username(username):
    return Professor.objects.get(user=username)


def create_professor_schedule_options(professor, owner, list_data):
    
    for data in list_data:
        p = ProfessorScheduleOptions.objects.create(professor=professor, owner=owner, schedule=data['schedule'])
        p.save()


def get_distribution_by_date(date):
    return Distribution.objects.get(start_date__lte = date, end_date__gte = date)


def distribute_classes():
    
    if Schedule.objects.filter(professor__isnull=False).exists():
        return Schedule.objects.all()
    
    professors = Professor.objects.all().order_by('position')

    for p in professors:
        options = ProfessorScheduleOptions.objects.filter(professor=p)

        for opt in options:
            if not opt.schedule.professor:

                opt.status = RequestStatus.ACEITO
                opt.schedule.professor = p
                opt.schedule.time_slot.available = False
                opt.save()

    return Schedule.objects.all()
    




