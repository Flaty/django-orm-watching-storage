from django.db import models
from django.utils.timezone import localtime, now


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def is_visit_long(visit, minutes=60):
    seconds_per_minute = 60
    return (visit.total_seconds() / seconds_per_minute) > minutes


def get_duration(visit):
    entered = visit.entered_at
    leaved = visit.leaved_at
    if leaved is None:
        return localtime(now()) - localtime(entered)
    return localtime(leaved) - localtime(entered)


def format_duration(duration):
    seconds = duration.total_seconds()
    seconds_per_hour = 3600
    seconds_per_minute = 60
    hours = seconds // seconds_per_hour
    minutes = (seconds % seconds_per_hour) // seconds_per_minute
    return f'{hours:g}ч {minutes:g}мин'
