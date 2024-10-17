from datacenter.models import Passcard, Visit, format_duration
from django.shortcuts import render
from django.utils.timezone import localtime, now
from django.shortcuts import get_object_or_404


def is_visit_long(visit, minutes=60):
    return (visit.total_seconds() / 60) > minutes


def get_duration(visit):
    entered = visit.entered_at
    leaved = visit.leaved_at
    if leaved is None:
        return localtime(now()) - localtime(entered)
    return localtime(leaved) - localtime(entered)


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []

    for visit in visits:
        duration = format_duration(get_duration(visit))
        flag = is_visit_long(get_duration(visit))
        
        temp = dict()
        temp['entered_at'] = localtime(visit.entered_at).strftime("%d %B %Y %H:%M")
        temp['duration'] = duration
        temp['is_strange'] = flag
        this_passcard_visits.append(temp)

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
