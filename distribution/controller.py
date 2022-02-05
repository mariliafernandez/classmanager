from .models import Professor


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
