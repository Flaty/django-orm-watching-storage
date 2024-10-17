from .models import Passcard, Visit
from .models import format_duration, is_visit_long, get_duration
from django.shortcuts import render
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []

    for visit in visits:
        duration = format_duration(get_duration(visit))
        has_long_visit = is_visit_long(get_duration(visit))
        visit_info = {
            'entered_at': localtime(visit.entered_at).strftime("%d %B %Y %H:%M"),
            'duration':  duration,
            'is_strange': has_long_visit,
        }
        this_passcard_visits.append(visit_info)

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
