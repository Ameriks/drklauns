from django.utils.translation import ugettext_lazy as _
from django.db import models

from drklauns.core.mixins import TimestampMixin


class Hospital(TimestampMixin, models.Model):
    name = models.CharField(_('Name of Hospital'), blank=True, max_length=255)

    def __str__(self):
        return self.name


class Department(TimestampMixin, models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(_('Name of Department'), blank=True, max_length=255)

    def __str__(self):
        return "%s - %s" % (self.hospital, self.name)
