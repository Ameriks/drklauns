import datetime

from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django import forms
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _


class AdminSplitDateTime(forms.SplitDateTimeWidget):
    """
    A SplitDateTime Widget that has some admin-specific styling.
    """
    def __init__(self, attrs=None):
        dt = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        choices = []
        for _ in range(0,1440,30):
            dt2 = dt + datetime.timedelta(minutes=_)
            choices.append((dt2.time(), str(dt2.time())[0:5]))

        widgets = [AdminDateWidget, forms.Select(choices=choices)]
        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
        # we want to define widgets.
        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        return format_html('<p class="datetime">{} {}<br />{} {}</p>',
                           _('Date:'), rendered_widgets[0],
                           _('Time:'), rendered_widgets[1])
