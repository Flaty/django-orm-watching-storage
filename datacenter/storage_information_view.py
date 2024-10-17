from django.shortcuts import render
from .models import Visit, get_duration, format_duration
from django.utils.timezone import localtime
import locale

locale.setlocale(locale.LC_TIME, '')


def storage_information_view(request):
    non_closed_visits = []
    visits = Visit.objects.filter(leaved_at=None)
    for visit in visits:
        visit_info = {
            'who_entered': visit.passcard.owner_name,
            'entered_at': localtime(visit.entered_at).strftime("%d %B %Y %H:%M"),
            'duration': format_duration(get_duration(visit)),
        }
        non_closed_visits.append(visit_info)

    context = {
        'non_closed_visits': non_closed_visits, 
    }
    return render(request, 'storage_information.html', context)
