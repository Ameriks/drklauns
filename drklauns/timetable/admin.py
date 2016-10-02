import datetime

from django import forms
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.contrib.admin.utils import unquote
from django.utils.translation import ugettext_lazy as _

from drklauns.timetable.export import monthly_excel
from drklauns.timetable.models import Work, Summary, Analytics
from drklauns.timetable.tasks import recalculate_summary
from drklauns.timetable.widgets import AdminSplitDateTime


def get_latest_edit_dt():
    now = timezone.now()
    latest_data_add = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if now.day < 8:
        latest_data_add = (latest_data_add - datetime.timedelta(days=1)).replace(day=1)
    return latest_data_add


class WorkAdminForm(forms.ModelForm):
    latest_data_add = None

    class Meta:
        model = Work
        fields = ('department', 'start', 'end', 'number_of_contacts', 'number_of_procedures', 'comments')
        widgets = {
            "start": AdminSplitDateTime,
            "end": AdminSplitDateTime,
        }

    class Media:
        js = ("js/project.js", )

    def __init__(self, *args, **kwargs):
        self.latest_data_add = get_latest_edit_dt()
        super().__init__(*args, **kwargs)
        print(self.fields['end'].widget)

    def clean_start(self):
        start = self.cleaned_data.get('start')

        if start < self.latest_data_add:
            if not (self.latest_data_add.year == 2016 and self.latest_data_add.month in (9, 10) and start.year == 2016):
                raise forms.ValidationError(_("Cannot add so far in past."))
        elif start > timezone.now():
            raise forms.ValidationError(_("Cannot add hours in future."))

        return start

    def clean_end(self):
        start = self.cleaned_data.get('start')
        end = self.cleaned_data.get('end')
        if not start:
            return end
        diff = (end - start).total_seconds() / 3600

        if end < start:
            raise forms.ValidationError(_("End cannot be before Start datetime"))
        elif end > timezone.now():
            raise forms.ValidationError(_("Cannot add hours in future."))
        elif diff > 8.0:
            raise forms.ValidationError(_("One work can be max 8 hours long."))
        elif diff < 1.0:
            raise forms.ValidationError(_("One work can be min 1 hour long."))

        return end


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_filter = ('employee', )
    list_display = ('employee', 'department', 'start', 'hours_worked', 'number_of_contacts', 'number_of_procedures')
    fields = ('department', 'start', 'end', 'number_of_contacts', 'number_of_procedures', 'comments')
    form = WorkAdminForm
    ordering = ('-start', )
    date_hierarchy = 'start'

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.modified_by = request.user
        if not obj.id:
            obj.employee = request.user
        obj.hours_worked = round((form.cleaned_data.get('end') - form.cleaned_data.get('start')).total_seconds() / 3600, 1)
        obj.save()
        recalculate_summary(work=obj)

    def has_change_permission(self, request, obj=None):
        if not obj or request.user.has_perm("timetable.change_all_work"):
            return super().has_change_permission(request, obj)

        if obj:
            latest_edit = get_latest_edit_dt()
            if obj.end < latest_edit:
                return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj:
            latest_edit = get_latest_edit_dt()
            if obj.end < latest_edit:
                return False
        return super().has_change_permission(request, obj)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.has_perm("timetable.view_all_work"):
            queryset = queryset.filter(created_by=request.user)

        return queryset


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_filter = ('employee', )
    list_display = ('employee', 'date', 'hours_worked', 'income', 'total_contacts', 'total_procedures')
    # fields = ('department', 'start', 'end', 'number_of_contacts', 'number_of_procedures', 'comments')
    readonly_fields = [field.name for field in Summary._meta.fields]
    date_hierarchy = 'date'

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    ordering = ('-year', '-month', )
    readonly_fields = [field.name for field in Analytics._meta.fields]
    change_form_template = "timetable/analytics.html"
    list_display = ("year", "month", "export_field", )

    def export_field(self, obj):
        return '<a href="%s">XLS</a>' % (reverse("admin:timetable_analytics_export", args=(obj.id, )))
    export_field.allow_tags = True
    export_field.short_description = _("Get XLS")

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        Analytics.objects.get_or_create(year=timezone.now().year, month=timezone.now().month)
        return super().changelist_view(request, extra_context)

    def get_urls(self):
        urlpatterns = super().get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        from django.conf.urls import url
        urlpatterns.insert(5, url(r'^(.+)/export/$', self.export_view, name='%s_%s_export' % info),)
        return urlpatterns

    def export_view(self, request, object_id, extra_context=None):
        obj = self.get_object(request, unquote(object_id))

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        file_obj = monthly_excel(year=obj.year, month=obj.month)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=analytics_%s-%s.xls' % (obj.year, obj.month)
        response.write(file_obj.getvalue())
        file_obj.close()
        return response

