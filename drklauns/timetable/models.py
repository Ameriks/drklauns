import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _

from drklauns.core.mixins import TimestampMixin


class Work(TimestampMixin, models.Model):
    employee = models.ForeignKey("users.User", verbose_name=_("Employee"))
    start = models.DateTimeField(_('Start of Work'))
    end = models.DateTimeField(_('End of Work'))
    hours_worked = models.FloatField(default=0)

    department = models.ForeignKey("core.Department", verbose_name=_("Department"))

    number_of_contacts = models.PositiveIntegerField(_("Number of Contacts"))
    number_of_procedures = models.PositiveIntegerField(_("Number of Procedures"))

    comments = models.TextField(_("Comments"), blank=True)

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view_all', 'change_all')
        verbose_name = _("Work object")
        verbose_name_plural = _("Work object")


class Summary(models.Model):
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True)

    date = models.DateField(_("Summary Month"))
    employee = models.ForeignKey("users.User", verbose_name=_("Employee"))

    hours_worked = models.FloatField(default=0)
    total_contacts = models.PositiveIntegerField(default=0)
    total_procedures = models.PositiveIntegerField(default=0)

    rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    income = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = _("Summary")

    def save(self, *args, **kwargs):
        self.income = round(self.hours_worked * float(self.rate), 2)
        return super().save(*args, **kwargs)

    def __str__(self):
        return "%s %s-%s" % (self.employee, self.date.year, self.date.month)


class Analytics(models.Model):
    year = models.PositiveIntegerField(_("Year"))
    month = models.PositiveSmallIntegerField(_("Month"))

    class Meta:
        verbose_name_plural = _("Analytics")

    def __str__(self):
        return "%s - %s" % (self.year, self.month)
