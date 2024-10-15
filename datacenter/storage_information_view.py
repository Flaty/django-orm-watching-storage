from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration
from django.utils.timezone import localtime
import locale

locale.setlocale(locale.LC_TIME, '')


def format_duration(duration):
    seconds = duration.total_seconds()
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f'{hours:g}ч {minutes:g}мин'


def storage_information_view(request):
    # Программируем здесь
    non_closed_visits = []
    visitor = Visit.objects.filter(leaved_at=None)
    for i in range(len(visitor)):
        temp = dict()
        temp['who_entered'] = visitor[i].passcard.owner_name
        temp['entered_at'] = localtime(visitor[i].entered_at).strftime("%d %B %Y %H:%M")
        temp['duration'] = format_duration(get_duration(visitor[i]))
        non_closed_visits.append(temp)

    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    print(non_closed_visits)
    return render(request, 'storage_information.html', context)
