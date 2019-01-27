from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimestampMixin(models.Model):
    class Meta:
        abstract = True
    created_by = models.ForeignKey('users.User', related_name='created_%(class)s_set', null=True, blank=True, on_delete=models.PROTECT)
    modified_by = models.ForeignKey('users.User', related_name='modified_%(class)s_set', null=True, blank=True, on_delete=models.PROTECT)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True)
