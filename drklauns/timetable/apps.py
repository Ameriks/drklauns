from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TimetableConfig(AppConfig):
    name = 'drklauns.timetable'
    verbose_name = _("Timetable")
