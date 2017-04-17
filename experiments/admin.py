from django.contrib import admin
from experiments.models import Experiment, ExperimentSet

# Register your models here.
class ExpSetAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'date_run')
    list_display = ('id', 'date_run')
admin.site.register(ExperimentSet, ExpSetAdmin)

class ExperimentAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'date_run')
    list_display = ('id', 'date_run')
admin.site.register(Experiment, ExperimentAdmin)
