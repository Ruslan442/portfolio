from django.contrib import admin
from import_export.admin import ExportActionMixin
from .models import Student, Projects, Events, ParticipationInEvents, ParticipationResults, ParticipationInProjects


class ParticipationInEventsInline(admin.TabularInline):
    model = ParticipationInEvents
    extra = 1


class ParticipationInProjectsInline(admin.TabularInline):
    model = ParticipationInProjects
    extra = 1


class StudentAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ["first_name", "last_name", 'course']
    list_filter = ['course']
    search_fields = ["last_name"]
    fieldsets = [
        ("Общие данные", {"fields": ["first_name", "last_name", "course"]}),
    ]
    inlines = [ParticipationInEventsInline, ParticipationInProjectsInline]


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ['title', 'creation_date']
    search_fields = ["title"]
    date_hierarchy = 'creation_date'
    list_display_links = ['title']
    readonly_fields = ['creation_date']


class EventsAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'was_held_recently']
    search_fields = ["title"]
    list_filter = ['date']
    date_hierarchy = 'date'
    list_display_links = ['title']
    readonly_fields = ['date']


class ParticipationResultsAdmin(admin.ModelAdmin):
    list_display = ['student', 'event', 'project', 'grade']
    list_filter = ['event']
    search_fields = ["student"]


class ParticipationInProjectsAdmin(admin.ModelAdmin):
    list_display = ['student', 'project']
    list_filter = ['project']
    search_fields = ["student"]


class ParticipationInEventsAdmin(admin.ModelAdmin):
    list_display = ['student', 'event']
    list_filter = ['event']
    search_fields = ["student"]


admin.site.register(Student, StudentAdmin)
admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Events, EventsAdmin)
admin.site.register(ParticipationResults, ParticipationResultsAdmin)
admin.site.register(ParticipationInProjects, ParticipationInProjectsAdmin)
admin.site.register(ParticipationInEvents, ParticipationInEventsAdmin)
