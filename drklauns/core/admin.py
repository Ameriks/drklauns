from django.contrib import admin

from drklauns.core.models import Hospital, Department


class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', )


class DepartmentAdmin(admin.ModelAdmin):
    list_filter = ('hospital', )
    list_display = ('name', 'hospital', )


admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Department, DepartmentAdmin)
